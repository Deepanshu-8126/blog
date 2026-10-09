import type { RawSignal } from './gtrends';

export async function fetchYouTubeTrending(apiKey?: string): Promise<RawSignal[]> {
  if (!apiKey) {
    // Graceful degrade if API key not yet configured in wrangler secret
    return [];
  }

  const url = `https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&chart=mostPopular&regionCode=IN&maxResults=15&key=${apiKey}`;

  try {
    const res = await fetch(url);
    if (!res.ok) {
      console.warn(`[youtube]: API responded with status ${res.status}`);
      return [];
    }

    const data = await res.json() as any;
    const items: RawSignal[] = [];
    let rank = 1;

    for (const vid of data.items || []) {
      const title = vid.snippet?.title || '';
      const viewCount = parseInt(vid.statistics?.viewCount || '100000', 10);
      const videoId = vid.id;

      if (title) {
        items.push({
          source: 'youtube',
          term: title,
          value: viewCount,
          rank: rank++,
          url: `https://www.youtube.com/watch?v=${videoId}`,
          meta: {
            channel: vid.snippet?.channelTitle,
            publishedAt: vid.snippet?.publishedAt
          }
        });
      }
    }

    return items;
  } catch (err) {
    console.warn('[youtube]: Fetch error:', err);
    return [];
  }
}
