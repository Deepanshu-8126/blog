export interface NicheMatch {
  slug: string;
  name: string;
  confidence: number;
}

const NICHE_RULES: Array<{
  slug: string;
  name: string;
  keywords: RegExp[];
  priority: number;
}> = [
  {
    slug: 'gta-6',
    name: 'GTA 6',
    keywords: [
      /\bgta\s*6\b/i,
      /\bgta\s*vi\b/i,
      /\bgrand\s*theft\s*auto\b/i,
      /\brockstar\s*games\b/i,
      /\bvice\s*city\b/i
    ],
    priority: 100
  },
  {
    slug: 'gold-rate',
    name: 'Gold Rate',
    keywords: [
      /\bgold\s*(?:rate|price|gram|bullion|mcx|24k|22k)?\b/i,
      /\bsilver\s*(?:rate|price|mcx)\b/i,
      /\bbullion\b/i,
      /\bsovereign\s*gold\b/i,
      /\bjewellery\b/i,
      /\bcarat\b/i,
      /\bkarat\b/i
    ],
    priority: 90
  },
  {
    slug: 'pc-builds',
    name: 'PC Builds',
    keywords: [
      /\b(?:rtx|gtx)\s*\d{3,4}\b/i,
      /\b(?:gpu|cpu|vram|ddr4|ddr5|nvme|ssd)\b/i,
      /\b(?:nvidia|geforce|radeon|intel|amd|ryzen|core\s*i[3579])\b/i,
      /\b(?:pc\s*build|gaming\s*pc|rig|motherboard|cabinet|graphics\s*card)\b/i,
      /\b(?:steam\s*deck|playstation|ps5|xbox)\b/i
    ],
    priority: 85
  },
  {
    slug: 'ai-tools',
    name: 'AI Tools',
    keywords: [
      /\b(?:chatgpt|gpt-4|gpt-5|openai|gemini|claude|anthropic)\b/i,
      /\b(?:deepseek|deepfake|midjourney|suno|elevenlabs|copilot|cursor)\b/i,
      /\b(?:generative\s*ai|artificial\s*intelligence|large\s*language\s*model|llm)\b/i,
      /\b(?:ai\s*agent|ai\s*tool|ai\s*model|prompt\s*engineering)\b/i
    ],
    priority: 85
  },
  {
    slug: 'health',
    name: 'Health',
    keywords: [
      /\b(?:medicine|medicines|medical|pharma|pharmaceutical)\b/i,
      /\b(?:doctor|hospital|clinic|patient|treatment|cure|symptoms)\b/i,
      /\b(?:ayurveda|ayurvedic|homeopathy|paracetamol|antibiotic)\b/i,
      /\b(?:fitness|diet|nutrition|workout|gym|protein|creatine|vitamin)\b/i,
      /\b(?:disease|virus|infection|cancer|diabetes|blood\s*pressure)\b/i,
      /\b(?:mental\s*health|depression|anxiety|wellness|sleep)\b/i
    ],
    priority: 80
  },
  {
    slug: 'side-hustles',
    name: 'Side Hustles',
    keywords: [
      /\b(?:side\s*hustle|freelance|freelancing|remote\s*job|work\s*from\s*home)\b/i,
      /\b(?:earn\s*money|passive\s*income|online\s*earning|dropshipping)\b/i,
      /\b(?:gig\s*worker|upwork|fiverr|affiliate\s*marketing)\b/i
    ],
    priority: 75
  },
  {
    slug: 'cashback',
    name: 'Cashback',
    keywords: [
      /\b(?:cashback|credit\s*card\s*reward|reward\s*points)\b/i,
      /\b(?:cred|cashkaro|earnkaro|upi\s*cashback)\b/i
    ],
    priority: 70
  },
  {
    slug: 'deals',
    name: 'Deals',
    keywords: [
      /\b(?:deal|deals|loot|discount|discounts|promo\s*code|coupon)\b/i,
      /\b(?:amazon\s*sale|flipkart\s*sale|great\s*indian\s*festival|big\s*billion)\b/i,
      /\b(?:flat\s*\d+%\s*off|price\s*drop|clearance\s*sale)\b/i
    ],
    priority: 65
  },
  {
    slug: 'movies',
    name: 'Movies',
    keywords: [
      /\b(?:movie|movies|film|cinema|box\s*office|trailer|teaser)\b/i,
      /\b(?:netflix|hotstar|prime\s*video|ott\s*release|review)\b/i,
      /\b(?:bollywood|hollywood|tollywood|kollywood|actor|actress)\b/i,
      /\b(?:season\s*\d+|episode|web\s*series)\b/i
    ],
    priority: 60
  },
  {
    slug: 'food',
    name: 'Food',
    keywords: [
      /\b(?:recipe|recipes|street\s*food|cooking|cuisine|dish|dishes)\b/i,
      /\b(?:zomato|swiggy|restaurant|biryani|paneer|kitchen)\b/i
    ],
    priority: 55
  },
  {
    slug: 'fashion',
    name: 'Fashion',
    keywords: [
      /\b(?:fashion|sneakers|sneaker|outfit|outfits|apparel|streetwear)\b/i,
      /\b(?:zara|h&m|nike|adidas|puma|clothing\s*brand)\b/i
    ],
    priority: 50
  }
];

/**
 * Maps any topic title, search term, or contextual signals to one of the 12 canonical niches.
 * Defaults cleanly to 'viral' (Entertainment & General Viral) if no niche-specific trigger matches.
 */
export function mapTopicToNiche(title: string, contextText = ''): { slug: string; name: string } {
  const combined = `${title} ${contextText}`.toLowerCase();

  for (const rule of NICHE_RULES) {
    for (const kw of rule.keywords) {
      if (kw.test(combined)) {
        return { slug: rule.slug, name: rule.name };
      }
    }
  }

  // Fallback to 'viral' (Entertainment & Viral Trends)
  return { slug: 'viral', name: 'Viral' };
}
