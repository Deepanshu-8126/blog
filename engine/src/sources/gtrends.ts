export interface RawSignal {
  source: string;
  term: string;
  value?: number;
  rank?: number;
  url?: string;
  approx_traffic?: string;
  meta?: any;
}

export async function fetchGoogleTrends(): Promise<RawSignal[]> {
  const url = 'https://trends.google.com/trending/rss?geo=IN';
  try {
    const res = await fetch(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
      }
    });

    if (!res.ok) {
      console.warn(`[gtrends]: Fetch failed with status ${res.status}`);
      return [];
    }

    const xml = await res.text();
    const items: RawSignal[] = [];

    // Lightweight defensive regex parser for RSS XML
    const itemRegex = /<item>([\s\S]*?)<\/item>/gi;
    let match: RegExpExecArray | null;
    let rank = 1;

    while ((match = itemRegex.exec(xml)) !== null) {
      const block = match[1];

      const titleMatch = /<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?<\/title>/i.exec(block);
      const trafficMatch = /<ht:approx_traffic>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?<\/ht:approx_traffic>/i.exec(block);
      const linkMatch = /<link>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?<\/link>/i.exec(block);
      const pictureMatch = /<ht:picture>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?<\/ht:picture>/i.exec(block);
      const pictureSourceMatch = /<ht:picture_source>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?<\/ht:picture_source>/i.exec(block);

      const title = titleMatch ? titleMatch[1].trim() : '';
      const trafficStr = trafficMatch ? trafficMatch[1].trim() : '';
      const link = linkMatch ? linkMatch[1].trim() : '';
      const picture = pictureMatch ? pictureMatch[1].trim() : '';
      const pictureSource = pictureSourceMatch ? pictureSourceMatch[1].trim() : '';

      if (title) {
        // Extract numeric floor value from "200K+", "50K+"
        let val = 10000;
        if (trafficStr.includes('K')) {
          val = parseFloat(trafficStr.replace(/[^\d.]/g, '')) * 1000;
        } else if (trafficStr.includes('M')) {
          val = parseFloat(trafficStr.replace(/[^\d.]/g, '')) * 1000000;
        } else if (trafficStr.includes('+')) {
          val = parseFloat(trafficStr.replace(/[^\d.]/g, '')) || val;
        }

        items.push({
          source: 'gtrends',
          term: title,
          value: val,
          rank: rank++,
          url: link,
          approx_traffic: trafficStr || `${val}+`,
          meta: {
            captured_at: new Date().toISOString(),
            picture,
            picture_source: pictureSource
          }
        });
      }
    }

    return items;
  } catch (err) {
    console.warn('[gtrends]: Parser exception:', err);
    return [];
  }
}
