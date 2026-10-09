import { fetchGoogleTrends, type RawSignal } from './sources/gtrends';
import { fetchGoogleNews } from './sources/gnews';
import { fetchWikimediaTop } from './sources/wiki';
import { fetchYouTubeTrending } from './sources/youtube';
import { fetchHackerNews } from './sources/hn';
import { fetchTMDBTrending } from './sources/tmdb';
import { normalizeTerm, resolveEntity, type ExistingTopic } from './resolve';
import { computeHypeScore, type SourceObservation, DEFAULT_SOURCE_WEIGHTS } from './score';
import { evaluateGate } from './gate';
import { writePipelineOutput, type TrendItemOutput, type D1BatchItem } from './write';
import { mapTopicToNiche } from './mapper';
import { autoWritePosts } from './writer';

export interface Env {
  DB?: any;
  KV?: any;
  YT_API_KEY?: string;
  TMDB_API_KEY?: string;
  GEMINI_API_KEY?: string;
  GEMINI_MODEL?: string;
  TELEGRAM_BOT_TOKEN?: string;
  TELEGRAM_CHAT_ID?: string;
}

export const NICHE_SEARCH_QUERIES: Record<string, string> = {
  'ai-tools': 'AI tools OR ChatGPT OR DeepSeek OR Claude OR LLM',
  'pc-builds': 'RTX 5090 OR RTX 4060 OR Ryzen gaming PC build India',
  'gold-rate': 'Gold rate India today OR 24K gold price MCX bullion',
  'deals': 'Amazon Great Indian Festival sale loot deals discount',
  'side-hustles': 'remote side hustles freelance work India 2026',
  'cashback': 'Credit card cashback offers Flipkart Amazon UPI rewards',
  'health': 'fitness diet whey protein Ayurvedic health routine',
  'fashion': 'streetwear fashion sneakers trends India',
  'food': 'high protein vegetarian diet Indian recipes nutrition',
  'gta-6': 'GTA 6 release date PC system requirements Rockstar Games',
  'movies': 'box office OTT release date Netflix Prime Video Bollywood'
};

export default {
  // 1. Cron Trigger Handler
  async scheduled(event: ScheduledEvent, env: Env, ctx: ExecutionContext): Promise<void> {
    const cron = event.cron;
    console.log(`[Engine]: Triggered scheduled job with cron: ${cron}`);
    const isHourly = cron === '7 * * * *';

    ctx.waitUntil(runEnginePipeline(env, isHourly, undefined, isHourly));
  },

  // 2. HTTP Fetch Handler
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);

    if (url.pathname === '/health') {
      return new Response(JSON.stringify({
        status: 'healthy',
        time: new Date().toISOString(),
        niches: Object.keys(NICHE_SEARCH_QUERIES).concat('viral'),
        sources: ['gtrends', 'gnews', 'wiki', 'youtube', 'hn', 'tmdb']
      }), {
        headers: { 'Content-Type': 'application/json' }
      });
    }

    if (url.pathname === '/trigger-all-niches' || (url.pathname === '/run' && url.searchParams.get('all_niches') === '1')) {
      const result = await runEnginePipeline(env, true, undefined, true);
      return new Response(JSON.stringify({
        success: true,
        mode: 'all_12_niches',
        count: result.boardItems.length,
        writer: result.writerStats,
        items: result.boardItems.slice(0, 15)
      }), {
        headers: { 'Content-Type': 'application/json' }
      });
    }

    if (url.pathname === '/trigger-niche') {
      const niche = url.searchParams.get('niche') || 'ai-tools';
      const result = await runEnginePipeline(env, false, niche);
      return new Response(JSON.stringify({
        success: true,
        mode: `single_niche_${niche}`,
        count: result.boardItems.length,
        writer: result.writerStats,
        items: result.boardItems.slice(0, 10)
      }), {
        headers: { 'Content-Type': 'application/json' }
      });
    }

    if (url.pathname === '/run') {
      const isHourly = url.searchParams.get('hourly') === '1';
      const result = await runEnginePipeline(env, isHourly);
      return new Response(JSON.stringify({
        success: true,
        count: result.boardItems.length,
        writer: result.writerStats,
        items: result.boardItems.slice(0, 10)
      }), {
        headers: { 'Content-Type': 'application/json' }
      });
    }

    return new Response('UniqueDigit Hype Engine Worker active. Use /run, /trigger-all-niches, or /trigger-niche?niche=ai-tools', {
      status: 200
    });
  }
};

async function runEnginePipeline(
  env: Env, 
  isHourly = false, 
  targetNiche?: string, 
  allNiches = false
): Promise<{ boardItems: TrendItemOutput[]; writerStats: any }> {
  console.log(`[Engine]: Running Multi-Signal Pipeline across sources (allNiches: ${allNiches}, targetNiche: ${targetNiche || 'none'})...`);

  // Check Engine Pause Switch from KV (File 7 §8: cfg:engine.paused)
  let isPaused = false;
  if (env.KV && typeof env.KV.get === 'function') {
    try {
      const cfg = await env.KV.get('cfg:engine', { type: 'json' }) as any;
      if (cfg && cfg.paused) {
        console.log('[Engine]: Engine publishing is paused via KV cfg:engine.paused');
        isPaused = true;
      }
    } catch {}
  }

  // Load Dynamic Weights from D1 sources table if available (Single query)
  let dynamicWeights = DEFAULT_SOURCE_WEIGHTS;
  if (env.DB && typeof env.DB.prepare === 'function') {
    try {
      const srcRows = await env.DB.prepare('SELECT key, weight FROM sources WHERE enabled = 1').all();
      if (srcRows.results && srcRows.results.length > 0) {
        dynamicWeights = {};
        for (const r of srcRows.results) {
          dynamicWeights[r.key] = r.weight;
        }
      }
    } catch (err) {
      console.warn('[Engine]: Could not load dynamic source weights, using defaults');
    }
  }

  // Step 1: Ingest raw signals concurrently from general sources
  const [gtrends, gnews, wiki, youtube, hn, tmdb] = await Promise.all([
    fetchGoogleTrends(),
    fetchGoogleNews(),
    fetchWikimediaTop(),
    fetchYouTubeTrending(env.YT_API_KEY),
    fetchHackerNews(),
    fetchTMDBTrending(env.TMDB_API_KEY)
  ]);

  // Step 1b: If allNiches or targetNiche is specified, ingest dedicated niche signals
  let targetedNicheSignals: RawSignal[] = [];
  if (allNiches || isHourly) {
    const nicheEntries = Object.entries(NICHE_SEARCH_QUERIES);
    const targetedResults = await Promise.all(
      nicheEntries.map(async ([_, query]) => {
        try {
          return await fetchGoogleNews(query);
        } catch {
          return [];
        }
      })
    );
    targetedNicheSignals = targetedResults.flat();
    console.log(`[Engine]: Ingested ${targetedNicheSignals.length} targeted signals across all niches`);
  } else if (targetNiche && NICHE_SEARCH_QUERIES[targetNiche]) {
    try {
      targetedNicheSignals = await fetchGoogleNews(NICHE_SEARCH_QUERIES[targetNiche]);
      console.log(`[Engine]: Ingested ${targetedNicheSignals.length} targeted signals for niche: ${targetNiche}`);
    } catch {}
  }

  const rawSignals: RawSignal[] = [
    ...gtrends,
    ...gnews,
    ...wiki,
    ...youtube,
    ...hn,
    ...tmdb,
    ...targetedNicheSignals
  ];

  console.log(`[Engine]: Ingested ${rawSignals.length} signals (gtrends: ${gtrends.length}, gnews: ${gnews.length}, wiki: ${wiki.length}, yt: ${youtube.length}, hn: ${hn.length}, tmdb: ${tmdb.length})`);

  // Identify healthy sources in this run
  const healthySources = new Set<string>();
  if (gtrends.length > 0) healthySources.add('gtrends');
  if (gnews.length > 0) healthySources.add('gnews');
  if (wiki.length > 0) healthySources.add('wiki');
  if (youtube.length > 0) healthySources.add('youtube');
  if (hn.length > 0) healthySources.add('hn');
  if (tmdb.length > 0) healthySources.add('tmdb');

  // Renormalize source weights to ONLY healthy & enabled sources for this run
  const healthyWeights: Record<string, number> = {};
  for (const [sKey, w] of Object.entries(dynamicWeights)) {
    if (healthySources.has(sKey)) {
      healthyWeights[sKey] = w;
    }
  }

  // Degraded Mode check: healthy independent sources < 3 pauses auto-promotion
  const INDEPENDENT_SOURCES = new Set(['gtrends', 'wiki', 'youtube', 'hn', 'tmdb', 'social']);
  let healthyIndependentCount = 0;
  for (const s of healthySources) {
    if (INDEPENDENT_SOURCES.has(s)) healthyIndependentCount++;
  }
  const isDegraded = healthyIndependentCount < 3;
  if (isDegraded) {
    console.warn(`[Engine]: WARNING: Only ${healthyIndependentCount} independent sources healthy. Running in DEGRADED mode (card/article generation paused).`);
  }

  // Build per-source value collections for exact percentile rank calculation
  const valuesBySource: Record<string, number[]> = {};
  for (const sig of rawSignals) {
    if (!valuesBySource[sig.source]) valuesBySource[sig.source] = [];
    if (typeof sig.value === 'number') valuesBySource[sig.source].push(sig.value);
  }

  // Step 2: Entity Resolution & Deduplication (with D1 History Preload)
  const existingTopics: ExistingTopic[] = [];
  const d1TopicsMap = new Map<string, { firstSeen: string; prevHype: number; prevGrowth: number }>();
  const pastSignalsMap = new Map<string, { value: number; diff: number }>();

  const nowMs = Date.now();
  const nowStr = new Date(nowMs).toISOString();
  const t48hAgo = new Date(nowMs - 48 * 3600 * 1000).toISOString();
  const t6hAgo = new Date(nowMs - 6 * 3600 * 1000).toISOString();
  const t3hAgo = new Date(nowMs - 3 * 3600 * 1000).toISOString();
  const targetVelocityMs = nowMs - 4.5 * 3600 * 1000; // Target center of 3-6h window

  if (env.DB && typeof env.DB.prepare === 'function') {
    try {
      // 1. Preload recent topics with first_seen (Bug 1 fix: use first_seen, NOT created_at)
      const recentTopics = await env.DB.prepare(
        'SELECT id, canonical, ckey, hype, growth, first_seen, last_seen FROM topics WHERE last_seen >= ?'
      ).bind(t48hAgo).all();

      if (recentTopics.results) {
        for (const row of recentTopics.results as any[]) {
          const { tokens } = normalizeTerm(row.canonical);
          existingTopics.push({
            id: row.id,
            canonical: row.canonical,
            ckey: row.ckey,
            tokens
          });
          d1TopicsMap.set(row.id, {
            firstSeen: row.first_seen || row.last_seen || nowStr,
            prevHype: row.hype || 0,
            prevGrowth: row.growth || 0
          });
        }
      }

      // 2. Query signals captured 3-6 hours ago using exact ISO bounds (Bug 2 fix)
      const pastSignals = await env.DB.prepare(
        'SELECT topic_id, source, value, captured_at FROM signals WHERE captured_at BETWEEN ? AND ?'
      ).bind(t6hAgo, t3hAgo).all();

      if (pastSignals.results) {
        for (const ps of pastSignals.results as any[]) {
          const rowMs = new Date(ps.captured_at).getTime() || 0;
          const diff = Math.abs(rowMs - targetVelocityMs);
          const sigKey = `${ps.topic_id}:${ps.source}`;
          const existing = pastSignalsMap.get(sigKey);
          // Pick snapshot closest to 4.5h ago
          if (!existing || diff < existing.diff) {
            pastSignalsMap.set(sigKey, { value: ps.value, diff });
          }
        }
      }
    } catch (err) {
      console.warn('[Engine]: Could not query historical topics/signals from D1:', err);
    }
  }

  const resolvedMap = new Map<string, {
    term: string;
    observations: SourceObservation[];
    approx?: string;
    rawList: RawSignal[];
  }>();

  for (const sig of rawSignals) {
    const { ckey, tokens } = normalizeTerm(sig.term);
    const resolved = resolveEntity(sig.term, existingTopics);

    const key = resolved.topicId || ckey;
    const prevVal = pastSignalsMap.get(`${key}:${sig.source}`)?.value;

    if (!resolvedMap.has(key)) {
      resolvedMap.set(key, {
        term: sig.term,
        observations: [{
          source: sig.source,
          value: sig.value || 1000,
          prevValue: prevVal,
          allSourceValues: valuesBySource[sig.source]
        }],
        approx: sig.approx_traffic,
        rawList: [sig]
      });
      existingTopics.push({
        id: key,
        canonical: sig.term,
        ckey,
        tokens
      });
    } else {
      const entry = resolvedMap.get(key)!;
      const alreadyHasSource = entry.observations.some(o => o.source === sig.source);
      if (!alreadyHasSource) {
        entry.observations.push({
          source: sig.source,
          value: sig.value || 1000,
          prevValue: prevVal,
          allSourceValues: valuesBySource[sig.source]
        });
      }
      entry.rawList.push(sig);
    }
  }

  // Step 3: Compute Hype Scores & Gates
  const boardItems: TrendItemOutput[] = [];
  const batchItems: D1BatchItem[] = [];

  for (const [key, item] of resolvedMap.entries()) {
    const hist = d1TopicsMap.get(key);
    const scored = computeHypeScore({
      topicId: key,
      firstSeenAt: hist?.firstSeen || nowStr,
      observations: item.observations,
      previousHype: hist?.prevHype,
      previousGrowth: hist?.prevGrowth,
      sourceWeights: healthyWeights
    });

    const gateDecision = evaluateGate({
      term: item.term,
      hype: scored.hype,
      nSources: scored.nSources,
      isEnginePaused: isPaused,
      isDegraded
    });

    if (gateDecision.action === 'ignored') {
      continue;
    }

    const slug = item.term
      .toLowerCase()
      .replace(/[^\w\s-]/g, '')
      .trim()
      .replace(/\s+/g, '-')
      .slice(0, 60);

    const h = scored.hype;
    const spark = [
      Math.max(10, Math.round(h * 0.55)),
      Math.max(15, Math.round(h * 0.70)),
      Math.max(20, Math.round(h * 0.82)),
      Math.max(25, Math.round(h * 0.92)),
      h
    ];

    const mapped = mapTopicToNiche(item.term);

    boardItems.push({
      id: key,
      title: item.term,
      slug,
      hype: scored.hype,
      growth: scored.growth,
      stage: scored.stage,
      n: scored.nSources,
      sources: item.observations.map(o => o.source),
      spark,
      niche: mapped.name,
      niche_slug: mapped.slug,
      approx_traffic: item.approx,
      updated_at: nowStr
    });

    batchItems.push({
      id: key,
      canonical: item.term,
      ckey: key,
      slug,
      hype: scored.hype,
      growth: scored.growth,
      stage: scored.stage,
      n_sources: scored.nSources,
      status: gateDecision.action,
      signals: item.rawList.map(r => ({
        source: r.source,
        value: r.value,
        rank: r.rank,
        url: r.url,
        meta: r.meta
      }))
    });
  }

  boardItems.sort((a, b) => b.hype - a.hype);

  // Step 4: Write to D1 (batch) and KV with signature comparison
  await writePipelineOutput(env, boardItems, batchItems, isHourly, isDegraded);

  // Step 4b: Auto-generate & Publish D1 Posts (Auto-Writer with Rate & Duplicate Protection)
  const writerStats = await autoWritePosts(env.DB, boardItems, batchItems, env);
  console.log(`[Engine]: Auto-Writer finished -> Created: ${writerStats.created}, Updated: ${writerStats.updated}, Skipped: ${writerStats.skipped}`);

  // Step 5: Telegram Alert with Strict Deduplication (Only once per topic)
  if (env.TELEGRAM_BOT_TOKEN && env.TELEGRAM_CHAT_ID && boardItems.length > 0) {
    const topDrop = boardItems[0];
    if (topDrop.hype >= 75) {
      const alertKey = `alerted:${topDrop.id}`;
      let alreadyAlerted = false;
      if (env.KV && typeof env.KV.get === 'function') {
        alreadyAlerted = Boolean(await env.KV.get(alertKey));
      }

      if (!alreadyAlerted) {
        try {
          const msg = `🚀 *HIGH HYPE ALERT (India)*\n\n*${topDrop.title}*\n🔥 Hype: ${topDrop.hype}/100\n📡 Sources: ${topDrop.sources.join(', ')}\n\nLive on: https://uniquedigit.in/trending`;
          await fetch(`https://api.telegram.org/bot${env.TELEGRAM_BOT_TOKEN}/sendMessage`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              chat_id: env.TELEGRAM_CHAT_ID,
              text: msg,
              parse_mode: 'Markdown'
            })
          });

          // Mark as alerted for 48 hours to prevent spamming
          if (env.KV && typeof env.KV.put === 'function') {
            await env.KV.put(alertKey, '1', { expirationTtl: 86400 * 2 });
          }
        } catch (err) {
          console.warn('[Engine]: Telegram alert send failure:', err);
        }
      }
    }
  }

  return { boardItems, writerStats };
}
