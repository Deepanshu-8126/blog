export interface SourceObservation {
  source: string;
  value: number;
  prevValue?: number; // Value from 3-6h earlier snapshot
  allSourceValues?: number[]; // Values distribution for percentile rank
}

export interface TopicScoreInput {
  topicId: string;
  firstSeenAt: string;
  observations: SourceObservation[];
  previousHype?: number;
  previousGrowth?: number;
  sourceWeights?: Record<string, number>; // Filtered to healthy/enabled sources only
  noSignal24h?: boolean;
}

export interface TopicScoreOutput {
  hype: number;
  growth: number;
  stage: 'emerging' | 'hot' | 'peak' | 'cooling' | 'gone';
  nSources: number;
  sourceScores: Record<string, { p_s: number; u_s: number; a_s: number }>;
}

export const DEFAULT_SOURCE_WEIGHTS: Record<string, number> = {
  gtrends: 0.30,
  gnews: 0.20,
  wiki: 0.15,
  youtube: 0.10,
  hn: 0.08,
  tmdb: 0.05,
  social: 0.12
};

// Floor baselines per source for growth calculation (File 7 §4)
export const SOURCE_FLOORS: Record<string, number> = {
  gtrends: 10000,
  gnews: 1000,
  wiki: 5000,
  youtube: 50000,
  hn: 20,
  tmdb: 10,
  social: 100
};

// Independent sources for corroboration 'n' (gnews excluded from independent n)
const INDEPENDENT_SOURCES = new Set(['gtrends', 'wiki', 'youtube', 'hn', 'tmdb', 'social']);

function sigmoid(x: number): number {
  return 1 / (1 + Math.exp(-x));
}

/**
 * Compute percentile rank. If sample size < 5, returns null (do not invent ranks on cold start)
 */
export function computePercentileRank(value: number, all?: number[]): number | null {
  if (!all || all.length < 5) return null;
  const countLte = all.filter(v => v <= value).length;
  return Math.max(0, Math.min(1, (countLte - 1) / Math.max(1, all.length - 1)));
}

export function computeHypeScore(input: TopicScoreInput): TopicScoreOutput {
  const obs = input.observations;
  if (!obs || obs.length === 0 || input.noSignal24h) {
    return {
      hype: 0,
      growth: -1,
      stage: 'gone',
      nSources: 0,
      sourceScores: {}
    };
  }

  // Caller passes only enabled & healthy sources in sourceWeights
  const weights = input.sourceWeights || DEFAULT_SOURCE_WEIGHTS;

  let totalActiveSystemWeight = 0;
  for (const s of Object.keys(weights)) {
    totalActiveSystemWeight += weights[s] || 0;
  }
  if (totalActiveSystemWeight <= 0) totalActiveSystemWeight = 1.0;

  let weightedBaseSum = 0;
  const sourceScores: Record<string, { p_s: number; u_s: number; a_s: number }> = {};
  let independentStrongSourcesCount = 0;

  for (const o of obs) {
    const sKey = o.source;
    const floor = SOURCE_FLOORS[sKey] || 1000;

    // 1) Percentile: if sample size is too small, treat as neutral (null -> 0.5)
    const pRaw = computePercentileRank(o.value, o.allSourceValues);
    const p_s = pRaw ?? 0.5;

    // 2) Velocity: neutral 0.5 if no previous history (do not bias new topics upwards)
    let u_s = 0.5;
    if (typeof o.prevValue === 'number' && o.prevValue > 0) {
      const g_s = (o.value - o.prevValue) / Math.max(o.prevValue, floor);
      u_s = sigmoid(2 * g_s);
    }

    // a_s = 0.6 * p_s + 0.4 * u_s
    const a_s = Math.max(0, Math.min(1, 0.6 * p_s + 0.4 * u_s));
    sourceScores[sKey] = { p_s, u_s, a_s };

    const normWeight = (weights[sKey] || 0.1) / totalActiveSystemWeight;
    weightedBaseSum += normWeight * a_s;

    // Strong source check: if percentile exists check >= 0.6, otherwise magnitude >= floor
    const strong = pRaw !== null ? pRaw >= 0.6 : o.value >= floor;
    if (strong && INDEPENDENT_SOURCES.has(sKey)) {
      independentStrongSourcesCount++;
    }
  }

  const base = Math.max(0, Math.min(1, weightedBaseSum));
  const n = independentStrongSourcesCount;
  const corro = Math.min(2.0, 1.0 + 0.25 * Math.max(0, n - 1));

  const firstSeenTs = new Date(input.firstSeenAt).getTime() || Date.now();
  const ageHours = Math.max(0, (Date.now() - firstSeenTs) / (1000 * 3600));
  const fresh = Math.exp(-Math.max(0, ageHours - 6) / 18);

  let rawHype = Math.round(Math.max(0, Math.min(100, 100 * base * corro * fresh)));

  // Strict anti-gaming constraint (File 7 §8): single source (n <= 1) cannot exceed 54
  if (n <= 1 && rawHype >= 55) {
    rawHype = 54;
  }

  let growth = 0.0;
  if (typeof input.previousHype === 'number' && input.previousHype > 0) {
    growth = parseFloat(((rawHype - input.previousHype) / input.previousHype).toFixed(2));
  }

  // 3) Stage Determination with hysteresis (User's Tested Patch)
  let stage: 'emerging' | 'hot' | 'peak' | 'cooling' | 'gone' = 'emerging';

  if (input.noSignal24h) {
    stage = 'gone';
  } else if (growth < -0.2 && (input.previousGrowth ?? 0) < -0.2) {
    // Requires 2 consecutive negative snapshots to mark cooling
    stage = 'cooling';
  } else if (rawHype >= 75 && Math.abs(growth) < 0.1 && n >= 2) {
    stage = 'peak';
  } else if (rawHype >= 55 && n >= 2) {
    stage = 'hot';
  } else {
    stage = 'emerging';
  }

  return {
    hype: rawHype,
    growth,
    stage,
    nSources: n,
    sourceScores
  };
}
