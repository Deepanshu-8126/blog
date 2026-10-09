import type { RawSignal } from './gtrends';

export async function fetchTMDBTrending(apiKey?: string): Promise<RawSignal[]> {
  if (!apiKey) {
    // Graceful degrade if API key not yet configured
    return [];
  }

  const url = `https://api.themoviedb.org/3/trending/movie/day?api_key=${apiKey}&region=IN`;

  try {
    const res = await fetch(url);
    if (!res.ok) return [];

    const data = await res.json() as any;
    const items: RawSignal[] = [];
    let rank = 1;

    for (const movie of data.results || []) {
      const title = movie.title || movie.original_title;
      const popularity = movie.popularity || 50;

      if (title && rank <= 12) {
        items.push({
          source: 'tmdb',
          term: title,
          value: popularity,
          rank: rank++,
          url: `https://www.themoviedb.org/movie/${movie.id}`,
          meta: {
            poster_path: movie.poster_path,
            overview: movie.overview,
            release_date: movie.release_date
          }
        });
      }
    }

    return items;
  } catch (err) {
    console.warn('[tmdb]: Fetch error:', err);
    return [];
  }
}
