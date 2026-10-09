export interface TrendItemOutput {
  id: string;
  title: string;
  slug: string;
  hype: number;
  growth: number;
  stage: 'emerging' | 'hot' | 'peak' | 'cooling' | 'gone';
  n: number;
  sources: string[];
  spark: number[];
  niche?: string;
  niche_slug?: string;
  approx_traffic?: string;
  updated_at: string;
}

export interface D1BatchItem {
  id: string;
  canonical: string;
  ckey: string;
  slug: string;
  hype: number;
  growth: number;
  stage: string;
  n_sources: number;
  status: string;
  signals: Array<{ source: string; value?: number; rank?: number; url?: string; meta?: any }>;
}

function computeBoardSignature(items: TrendItemOutput[]): string {
  return items.slice(0, 20).map(i => `${i.id}:${i.hype}:${i.stage}`).join('|');
}

export async function writePipelineOutput(
  env: any,
  board: TrendItemOutput[],
  batchItems: D1BatchItem[],
  isHourly = false,
  isDegraded = false
): Promise<void> {
  const db = env.DB;
  const kv = env.KV;
  const nowStr = new Date().toISOString();

  // 1. D1 Batch Writes: topics, signals, hype_history
  if (db && typeof db.prepare === 'function' && typeof db.batch === 'function') {
    try {
      const statements: any[] = [];

      for (const item of batchItems.slice(0, 30)) {
        statements.push(
          db.prepare(`
            INSERT INTO topics (id, canonical, ckey, slug, hype, growth, stage, n_sources, status, last_seen)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
              hype = excluded.hype,
              growth = excluded.growth,
              stage = excluded.stage,
              n_sources = excluded.n_sources,
              status = CASE WHEN topics.status IN ('card', 'article') THEN topics.status ELSE excluded.status END,
              last_seen = excluded.last_seen
          `).bind(
            item.id,
            item.canonical,
            item.ckey,
            item.slug,
            item.hype,
            item.growth,
            item.stage,
            item.n_sources,
            item.status,
            nowStr
          )
        );

        statements.push(
          db.prepare(`
            INSERT OR REPLACE INTO hype_history (topic_id, ts, hype)
            VALUES (?, ?, ?)
          `).bind(item.id, nowStr, item.hype)
        );

        for (const s of item.signals) {
          statements.push(
            db.prepare(`
              INSERT INTO signals (topic_id, source, value, rank, url, captured_at)
              VALUES (?, ?, ?, ?, ?, ?)
            `).bind(item.id, s.source, s.value || 0, s.rank || 0, s.url || '', nowStr)
          );
        }
      }

      statements.push(
        db.prepare(`
          INSERT INTO pipeline_runs (job, started_at, ok, summary)
          VALUES ('fast_ingest', ?, 1, ?)
        `).bind(nowStr, `Processed ${batchItems.length} topics, published top 30`)
      );

      if (statements.length > 0) {
        for (let i = 0; i < statements.length; i += 40) {
          await db.batch(statements.slice(i, i + 40));
        }
        console.log(`[writePipelineOutput]: Successfully wrote batch statements to D1`);
      }
    } catch (err) {
      console.error('[writePipelineOutput]: D1 batch write error:', err);
    }
  }

  // 2. Single Combined KV Key boards:v1 with Internal Signature (Strict Free Tier Protection)
  if (kv && typeof kv.put === 'function') {
    try {
      const top30 = board.slice(0, 30);
      const byNiche: Record<string, TrendItemOutput[]> = {};
      for (const item of board) {
        if (item.niche_slug) {
          if (!byNiche[item.niche_slug]) byNiche[item.niche_slug] = [];
          byNiche[item.niche_slug].push(item);
        }
      }

      const newSignature = computeBoardSignature(top30);

      let prevSignature: string | null = null;
      try {
        const prevData = await kv.get('boards:v1', { type: 'json' }) as any;
        if (prevData && prevData.sig) {
          prevSignature = prevData.sig;
        }
      } catch {}

      // Only write when signature changes: ~96 writes/day maximum
      if (prevSignature !== newSignature) {
        const payload = {
          sig: newSignature,
          global: top30,
          niches: byNiche,
          updated_at: nowStr,
          degraded: isDegraded
        };
        await kv.put('boards:v1', JSON.stringify(payload));
        console.log(`[writePipelineOutput]: Board content changed, updated single KV key boards:v1 (degraded=${isDegraded})`);
      } else {
        console.log(`[writePipelineOutput]: Board unchanged, skipped redundant KV write`);
      }
    } catch (err) {
      console.error('[writePipelineOutput]: KV put error:', err);
    }
  }
}
