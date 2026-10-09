import type { RawSignal } from './gtrends';

export async function fetchGoogleNews(topicQuery?: string): Promise<RawSignal[]> {
  const url = topicQuery
    ? `https://news.google.com/rss/search?q=${encodeURIComponent(topicQuery)}&hl=en-IN&gl=IN&ceid=IN:en`
    : `https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en`;

  try {
    const res = await fetch(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
      }
    });

    if (!res.ok) return [];

    const xml = await res.text();
    const items: RawSignal[] = [];

    const itemRegex = /<item>([\s\S]*?)<\/item>/gi;
    let match: RegExpExecArray | null;
    let rank = 1;

    while ((match = itemRegex.exec(xml)) !== null && rank <= 15) {
      const block = match[1];

      const titleMatch = /<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?<\/title>/i.exec(block);
      const linkMatch = /<link>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?<\/link>/i.exec(block);
      const pubDateMatch = /<pubDate>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?<\/pubDate>/i.exec(block);
      const sourceMatch = /<source[^>]*>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?<\/source>/i.exec(block);

      const rawTitle = titleMatch ? titleMatch[1].trim() : '';
      const link = linkMatch ? linkMatch[1].trim() : '';
      const publisher = sourceMatch ? sourceMatch[1].trim() : '';

      // Strip publisher suffix (" - NDTV", " - Times of India")
      const cleanTitle = rawTitle.replace(/\s+-\s+[^-]+$/, '').trim();

      if (cleanTitle) {
        items.push({
          source: 'gnews',
          term: cleanTitle,
          value: 15000 / rank,
          rank: rank++,
          url: link,
          meta: {
            publisher,
            pubDate: pubDateMatch ? pubDateMatch[1] : new Date().toISOString()
          }
        });
      }
    }

    return items;
  } catch (err) {
    console.warn('[gnews]: Fetch exception:', err);
    return [];
  }
}
