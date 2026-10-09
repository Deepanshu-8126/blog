const STOPWORDS = new Set([
  'live', 'score', 'news', 'today', 'vs', 'v', 'update', 'updates', 'price', 'prices',
  'in', 'india', 'latest', 'review', 'watch', 'how', 'to', 'what', 'is', 'the', 'a', 'an'
]);

export function normalizeTerm(term: string): { ckey: string; tokens: string[] } {
  const cleaned = term
    .toLowerCase()
    .replace(/[^\w\s]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();

  const rawTokens = cleaned.split(' ').filter(t => t.length > 1 && !STOPWORDS.has(t));
  const uniqueTokens = Array.from(new Set(rawTokens)).sort();
  const ckey = uniqueTokens.join('_');

  return { ckey, tokens: uniqueTokens };
}

export function jaccardSimilarity(tokensA: string[], tokensB: string[]): number {
  if (tokensA.length === 0 || tokensB.length === 0) return 0;
  const setA = new Set(tokensA);
  const setB = new Set(tokensB);

  let intersection = 0;
  for (const t of setA) {
    if (setB.has(t)) intersection++;
  }

  const union = setA.size + setB.size - intersection;
  return union > 0 ? intersection / union : 0;
}

export interface ExistingTopic {
  id: string;
  canonical: string;
  ckey: string;
  tokens: string[];
}

export function resolveEntity(term: string, existingTopics: ExistingTopic[]): { topicId?: string; isNew: boolean; ckey: string } {
  const { ckey, tokens } = normalizeTerm(term);

  // 1. Exact canonical key match
  const exact = existingTopics.find(t => t.ckey === ckey);
  if (exact) {
    return { topicId: exact.id, isNew: false, ckey };
  }

  // 2. Token Jaccard >= 0.6 match (as per File 7 §3)
  for (const t of existingTopics) {
    const sim = jaccardSimilarity(tokens, t.tokens);
    if (sim >= 0.6) {
      return { topicId: t.id, isNew: false, ckey: t.ckey };
    }
  }

  return { isNew: true, ckey };
}
