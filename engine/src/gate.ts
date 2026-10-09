export type TopicAction = 'ignored' | 'tracking' | 'board' | 'card' | 'article';

export interface GateInput {
  term: string;
  hype: number;
  nSources: number; // Must be independent sources (excluding gnews)
  nicheSlug?: string;
  blocklist?: string[];
  isSensitiveCategory?: boolean;
  consecutiveHighSnapshots?: number; // Must be >= 3 snapshots for article
  dailyCardsCount?: number;
  dailyArticlesCount?: number;
  isEnginePaused?: boolean; // KV cfg:engine.paused
  isDegraded?: boolean; // When healthy independent sources < 3
}

export interface GateDecision {
  action: TopicAction;
  reason: string;
  indexable: boolean;
  requiresReview: boolean;
}

const DEFAULT_BLOCKLIST = new Set([
  'suicide', 'murder', 'rape', 'death', 'killed', 'accident',
  'crime', 'adult', 'nude', 'porn', 'scam', 'violence'
]);

export function evaluateGate(input: GateInput): GateDecision {
  // 1. Kill Switch Check (KV cfg:engine.paused)
  if (input.isEnginePaused) {
    return {
      action: 'board',
      reason: 'Engine publishing paused via kill switch (tracking only)',
      indexable: false,
      requiresReview: false
    };
  }

  const lowerTerm = input.term.toLowerCase();

  // 2. Safety Blocklist Check
  const isBlocked = Array.from(DEFAULT_BLOCKLIST).some(term => lowerTerm.includes(term)) ||
    (input.blocklist && input.blocklist.some(term => lowerTerm.includes(term.toLowerCase())));

  if (isBlocked) {
    return {
      action: 'ignored',
      reason: 'Safety blocklist match (tragedy/adult/crime)',
      indexable: false,
      requiresReview: false
    };
  }

  // 3. Sensitive Niche Gate (Health / Finance) -> Draft review queue, never auto-publish
  if (input.isSensitiveCategory || input.nicheSlug === 'health' || lowerTerm.includes('cure') || lowerTerm.includes('stock tip')) {
    return {
      action: input.hype >= 55 ? 'card' : 'board',
      reason: 'YMYL Sensitive topic flagged for admin review',
      indexable: false,
      requiresReview: true
    };
  }

  // 4. Threshold Gates (File 7 §5)
  if (input.hype < 25) {
    return {
      action: 'tracking',
      reason: 'Hype below 25, tracking in background only',
      indexable: false,
      requiresReview: false
    };
  }

  if (input.hype < 55 || input.nSources < 2) {
    return {
      action: 'board',
      reason: 'Live board entry only (hype 25-54 or n < 2)',
      indexable: false,
      requiresReview: false
    };
  }

  // 5. Degraded Mode Guard: Pause card and article auto-promotions when independent sources < 3
  if (input.isDegraded) {
    return {
      action: 'board',
      reason: 'Degraded mode active (healthy independent sources < 3, auto card/article generation paused)',
      indexable: false,
      requiresReview: false
    };
  }

  // Article Promotion: Hype >= 70 sustained for >= 3 snapshots (File 7 §5) + Daily cap check
  const snapshots = input.consecutiveHighSnapshots || 1;
  const articlesCount = input.dailyArticlesCount || 0;
  if (input.hype >= 70 && input.nSources >= 2 && snapshots >= 3 && articlesCount < 30) {
    return {
      action: 'article',
      reason: 'High sustained hype (>=70 for >=3 snapshots) with multi-source corroboration',
      indexable: true,
      requiresReview: false
    };
  }

  // Auto Trend Card: Hype >= 55 and n >= 2 (Daily cap check: <= 60 cards)
  const cardsCount = input.dailyCardsCount || 0;
  if (cardsCount < 60) {
    return {
      action: 'card',
      reason: 'Hot trend card auto-generation (hype >= 55, n >= 2, noindex)',
      indexable: false,
      requiresReview: false
    };
  }

  return {
    action: 'board',
    reason: 'Daily card generation cap (60/day) reached, board entry only',
    indexable: false,
    requiresReview: false
  };
}
