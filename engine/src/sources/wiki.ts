import type { RawSignal } from './gtrends';

export async function fetchWikimediaTop(): Promise<RawSignal[]> {
  // Get yesterday's date (Wikimedia pageviews are daily compiled)
  const d = new Date(Date.now() - 86400000 * 2);
  const year = d.getUTCFullYear();
  const month = String(d.getUTCMonth() + 1).padStart(2, '0');
  const day = String(d.getUTCDate()).padStart(2, '0');

  const url = `https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia.org/all-access/${year}/${month}/${day}`;

  try {
    const res = await fetch(url, {
      headers: {
        'User-Agent': 'UniqueDigit-HypeBot/2.0 (https://uniquedigit.in; contact@uniquedigit.in)'
      }
    });

    if (!res.ok) return [];

    const data = await res.json() as any;
    const articles = data?.items?.[0]?.articles || [];
    const items: RawSignal[] = [];

    let rank = 1;
    // Exclude Wikipedia meta pages
    const EXCLUDE_PREFIXES = ['Main_Page', 'Special:', 'Portal:', 'Wikipedia:'];

    for (const art of articles) {
      if (rank > 15) break;
      const title = art.article.replace(/_/g, ' ');

      if (EXCLUDE_PREFIXES.some(prefix => title.startsWith(prefix))) {
        continue;
      }

      items.push({
        source: 'wiki',
        term: title,
        value: art.views || 50000,
        rank: rank++,
        url: `https://en.wikipedia.org/wiki/${encodeURIComponent(art.article)}`,
        meta: { views: art.views }
      });
    }

    return items;
  } catch (err) {
    console.warn('[wiki]: Fetch exception:', err);
    return [];
  }
}
