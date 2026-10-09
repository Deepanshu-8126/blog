import type { RawSignal } from './gtrends';

export async function fetchHackerNews(): Promise<RawSignal[]> {
  try {
    const res = await fetch('https://hacker-news.firebaseio.com/v0/topstories.json');
    if (!res.ok) return [];

    const ids = await res.json() as number[];
    const topIds = ids.slice(0, 15);

    const itemPromises = topIds.map(async (id, idx) => {
      try {
        const itemRes = await fetch(`https://hacker-news.firebaseio.com/v0/item/${id}.json`, {
          signal: AbortSignal.timeout(4000)
        });
        if (itemRes.ok) {
          const itemData = await itemRes.json() as any;
          if (itemData && itemData.title) {
            return {
              source: 'hn',
              term: itemData.title,
              value: itemData.score || 50,
              rank: idx + 1,
              url: itemData.url || `https://news.ycombinator.com/item?id=${id}`,
              meta: { comments: itemData.descendants || 0 }
            } as RawSignal;
          }
        }
      } catch {
        // Individual item skip
      }
      return null;
    });

    const results = await Promise.all(itemPromises);
    const items = results.filter((i): i is RawSignal => Boolean(i));
    return items;
  } catch (err) {
    console.warn('[hn]: Fetch error:', err);
    return [];
  }
}
