export interface NicheNavTab {
  id: string;
  label: string;
  icon?: string;
  href?: string;
}

export const NICHE_NAV_CONFIG: Record<string, NicheNavTab[]> = {
  feed: [
    { id: 'latest', label: 'Latest', icon: 'clock' },
    { id: 'trending', label: 'Trending', icon: 'sparkles' },
    { id: 'categories', label: 'Categories', icon: 'grid' },
  ],
  tools: [
    { id: 'all', label: 'All Tools', icon: 'sparkles' },
    { id: 'categories', label: 'Categories', icon: 'grid' },
    { id: 'compare', label: 'Compare', icon: 'git-compare' },
    { id: 'submit', label: 'Submit Tool', icon: 'plus', href: '/submit-tool' },
  ],
  dataset: [
    { id: 'live', label: 'Live Data', icon: 'activity' },
    { id: 'history', label: 'History', icon: 'clock' },
    { id: 'export', label: 'Export', icon: 'download' },
    { id: 'methodology', label: 'Methodology', icon: 'book' },
  ],
  movies: [
    { id: 'theatrical', label: 'In Theatres', icon: 'clapperboard' },
    { id: 'ott', label: 'OTT / Streaming', icon: 'tv' },
    { id: 'coming', label: 'Coming Soon', icon: 'calendar' },
    { id: 'reviews', label: 'Reviews', icon: 'star' },
  ],
  deals: [
    { id: 'live', label: 'Live Deals', icon: 'zap' },
    { id: 'categories', label: 'Categories', icon: 'grid' },
    { id: 'stores', label: 'Stores', icon: 'shopping-bag' },
    { id: 'alerts', label: 'Price Alerts', icon: 'bell' },
  ],
  health: [
    { id: 'latest', label: 'Latest', icon: 'clock' },
    { id: 'categories', label: 'Categories', icon: 'grid' },
    { id: 'tools', label: 'Equipment', icon: 'dumbbell' },
    { id: 'emergency', label: 'Emergency', icon: 'alert-triangle' },
  ],
};

export function getNicheNavTabs(pageType: string): NicheNavTab[] {
  return NICHE_NAV_CONFIG[pageType] || NICHE_NAV_CONFIG.feed;
}

export const GROUP_NICHES: Record<string, string[]> = {
  Tech: ['pc-builds', 'gold-rate', 'ai-tools', 'automotive-trends'],
  Money: ['deals', 'side-hustles', 'cashback'],
  Lifestyle: ['health', 'fashion', 'food'],
  Entertainment: ['gta-6', 'movies', 'viral', 'cricket-sports'],
  Education: ['exams-results'],
};