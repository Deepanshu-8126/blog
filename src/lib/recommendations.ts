/**
 * UniqueDigit Contextual Multi-Store Loot & Recommendation Engine
 * Dynamically connects user intent to high-commission affiliate deals:
 * - Amazon Direct (tag=uniquedigi0c6-21)
 * - EarnKaro / Direct (Myntra, Ajio, Meesho, Swiggy, Paytm, MakeMyTrip, Bank Cards)
 */

export interface ContextualDeal {
  title: string;
  category: string;
  badge: string;
  discount: string;
  merchant: 'Amazon' | 'Myntra / Ajio' | 'EarnKaro' | 'Swiggy / Zomato' | 'Bank / Cards' | 'MakeMyTrip' | 'Udemy' | 'Blinkit / Zepto / Instamart';
  affUrl: string;
  icon: string;
  priceNote?: string;
  trustTag: string;
}

const AMAZON_TAG = 'uniquedigi0c6-21';

export const NICHE_DEAL_MATRIX: Record<string, ContextualDeal[]> = {
  // Deals & Quick Commerce (Blinkit / Zepto / Amazon)
  'deals': [
    {
      title: 'Quick Commerce Flash Deals: Blinkit & Zepto 10-Minute Grocery & Tech Loot',
      category: '10-Min Flash Delivery',
      badge: '⚡ Flat 50% Off Code',
      discount: 'Instant ₹100 Cashback',
      merchant: 'Blinkit / Zepto / Instamart',
      affUrl: `https://www.amazon.in/s?k=daily+grocery+household+deals&tag=${AMAZON_TAG}`,
      icon: 'tag',
      priceNote: 'Live in Top 20 Indian Cities',
      trustTag: 'Verified Today'
    },
    {
      title: 'Amazon Lightning Deals: Electronics, Laptops & Smartphones Under ₹9,999',
      category: 'Electronics Loot',
      badge: '🔥 60% OFF',
      discount: 'Additional Bank Discount',
      merchant: 'Amazon',
      affUrl: `https://www.amazon.in/s?k=lightning+deals+electronics&tag=${AMAZON_TAG}`,
      icon: 'sparkles',
      priceNote: 'Limited Stock Offers',
      trustTag: 'Prime Fast Delivery'
    }
  ],
  // 1. Gaming / GTA 6 / PC Builds
  'gta-6': [
    {
      title: 'High-DPI RGB Gaming Mouse & Speed Mousepad',
      category: 'Gaming Gear',
      badge: '🔥 45% OFF',
      discount: 'Under ₹999 Loot',
      merchant: 'Amazon',
      affUrl: `https://www.amazon.in/s?k=gaming+mouse+rgb+mousepad&tag=${AMAZON_TAG}`,
      icon: 'gamepad',
      priceNote: 'Starting ₹499',
      trustTag: 'Prime 1-Day Delivery'
    },
    {
      title: '7.1 Surround Sound Gaming Headset with Mic',
      category: 'Audio & Streaming',
      badge: '⚡ Top Rated',
      discount: 'Up to 55% Off',
      merchant: 'Amazon',
      affUrl: `https://www.amazon.in/s?k=gaming+headphones+with+mic&tag=${AMAZON_TAG}`,
      icon: 'sparkles',
      priceNote: 'Tested for Discord & GTA',
      trustTag: '100% Genuine Warranty'
    }
  ],
  'pc-builds': [
    {
      title: 'NVIDIA RTX 4060 / 4070 & AMD GPUs Live Price Drops',
      category: 'PC Components',
      badge: '⚡ Live Drop',
      discount: 'Bank Discount ₹2,500',
      merchant: 'Amazon',
      affUrl: `https://www.amazon.in/s?k=graphic+card+rtx+4060&tag=${AMAZON_TAG}`,
      icon: 'cpu',
      priceNote: 'Verified Sellers Only',
      trustTag: 'Brand Indian Warranty'
    },
    {
      title: 'Gen4 1TB/2TB NVMe High Speed SSDs & DDR5 RAM',
      category: 'Storage & Memory',
      badge: '⭐ Amazon Choice',
      discount: 'Up to 60% Off',
      merchant: 'Amazon',
      affUrl: `https://www.amazon.in/s?k=1tb+nvme+ssd+gen4&tag=${AMAZON_TAG}`,
      icon: 'cpu',
      priceNote: '7000 MB/s Read Speed',
      trustTag: '5-Year Replacement'
    }
  ],

  // 2. Health & Ayurveda
  'health': [
    {
      title: '100% Whey Protein Isolate & Plant Protein Blends',
      category: 'Nutrition & Gym',
      badge: '💪 Best Seller',
      discount: '30% Off + Instant Coupon',
      merchant: 'Amazon',
      affUrl: `https://www.amazon.in/s?k=whey+protein+isolate+authentic&tag=${AMAZON_TAG}`,
      icon: 'heart',
      priceNote: 'Lab-Door Authenticated',
      trustTag: 'Direct Brand Fulfilled'
    },
    {
      title: 'Breathable Gym Wear, Dry-Fit Tees & Trackpants',
      category: 'Activewear Loot',
      badge: '🔥 Under ₹499',
      discount: 'Buy 2 Get Extra 15%',
      merchant: 'Myntra / Ajio',
      affUrl: `https://www.amazon.in/s?k=gym+wear+men+women+dry+fit&tag=${AMAZON_TAG}`,
      icon: 'shirt',
      priceNote: 'EarnKaro / Amazon Deal',
      trustTag: 'Easy 7-Day Return'
    }
  ],

  // 3. Gold Rate & Investment
  'gold-rate': [
    {
      title: '24K 999.9 Purity Certified Gold Coins & Bullion (MMTC-PAMP)',
      category: 'Gold & Bullion',
      badge: '🏆 Certified 999.9',
      discount: 'Zero Making Charges',
      merchant: 'Amazon',
      affUrl: `https://www.amazon.in/s?k=24k+gold+coin+mmtc+pamp&tag=${AMAZON_TAG}`,
      icon: 'coins',
      priceNote: 'Tamper-Proof CertiCard',
      trustTag: 'Insured Delivery'
    },
    {
      title: '999 Fine Silver Coins & Bars for Gifting / Savings',
      category: 'Precious Metals',
      badge: '⚡ Trending',
      discount: 'Live Market Rate',
      merchant: 'Amazon',
      affUrl: `https://www.amazon.in/s?k=999+fine+silver+coin&tag=${AMAZON_TAG}`,
      icon: 'coins',
      priceNote: 'Govt Hallmarked',
      trustTag: 'Secure Packing'
    }
  ],

  // 4. Movies & OTT
  'movies': [
    {
      title: 'Fire TV Stick 4K with Alexa Voice Remote',
      category: 'Home Theater',
      badge: '🎬 Bestseller',
      discount: 'Flat ₹1,500 Off',
      merchant: 'Amazon',
      affUrl: `https://www.amazon.in/s?k=fire+tv+stick+4k&tag=${AMAZON_TAG}`,
      icon: 'clapperboard',
      priceNote: 'Dolby Atmos & Vision',
      trustTag: 'Official Amazon Device'
    },
    {
      title: 'Dolby Audio Soundbar & Subwoofer Home Audio Systems',
      category: 'Audio Experience',
      badge: '⚡ 50% OFF',
      discount: 'Starting ₹2,999',
      merchant: 'Amazon',
      affUrl: `https://www.amazon.in/s?k=soundbar+for+tv+with+subwoofer&tag=${AMAZON_TAG}`,
      icon: 'sparkles',
      priceNote: 'Cinema Sound at Home',
      trustTag: 'Brand Warranty'
    }
  ],

  // 5. Fashion & Sneakers Loot (Myntra / Ajio / EarnKaro)
  'fashion': [
    {
      title: 'Branded Casual Sneakers & Streetwear (Puma, Red Tape, Nike)',
      category: 'Sneakers Loot',
      badge: '🔥 Flat 60-80% Off',
      discount: 'Under ₹999 Deals',
      merchant: 'Myntra / Ajio',
      affUrl: `https://www.amazon.in/s?k=sneakers+shoes+for+men+offers&tag=${AMAZON_TAG}`,
      icon: 'shirt',
      priceNote: 'Top Rated Styles',
      trustTag: '100% Original Guarantee'
    },
    {
      title: 'Trending Titan & Fastrack Smartwatches & Premium Watches',
      category: 'Fashion Accessories',
      badge: '⚡ Under ₹499 - ₹1,499',
      discount: 'Special Flash Sale',
      merchant: 'Amazon',
      affUrl: `https://www.amazon.in/s?k=smartwatch+bluetooth+calling+offers&tag=${AMAZON_TAG}`,
      icon: 'sparkles',
      priceNote: 'AMOLED Display Options',
      trustTag: 'Official Warranty'
    }
  ],

  // 6. Cashback & Banking / Credit Cards (Highest Payouts)
  'cashback': [
    {
      title: 'Lifetime FREE Cashback Credit Cards (5% Unlimited Online Cashback)',
      category: 'Bank Rewards',
      badge: '💎 ₹1,500 Welcome Bonus',
      discount: 'Zero Annual Fee',
      merchant: 'Bank / Cards',
      affUrl: `https://www.amazon.in/s?k=amazon+pay+icici+credit+card&tag=${AMAZON_TAG}`,
      icon: 'percent',
      priceNote: 'Instant Digital Approval',
      trustTag: '100% Secure & RBI Regulated'
    },
    {
      title: 'Mobile Recharge & Bill Pay Cashback Offers (Flat ₹50 - ₹100 Back)',
      category: 'Bill Payments',
      badge: '⚡ Daily Code',
      discount: 'UPI & Wallet Cashback',
      merchant: 'EarnKaro',
      affUrl: `https://www.amazon.in/s?k=mobile+recharge+offers&tag=${AMAZON_TAG}`,
      icon: 'percent',
      priceNote: 'Valid on Airtel, Jio, VI',
      trustTag: 'Verified Today'
    }
  ],

  // 7. AI Tools & Learning (Courses, SaaS)
  'ai-tools': [
    {
      title: 'High-Performance Laptops for AI Coding & Prompt Engineering',
      category: 'Workstation Laptops',
      badge: '⚡ Intel Core i7 / M3 Deals',
      discount: 'Up to ₹25,000 Off on Exchange',
      merchant: 'Amazon',
      affUrl: `https://www.amazon.in/s?k=laptops+for+programming+ai&tag=${AMAZON_TAG}`,
      icon: 'cpu',
      priceNote: '16GB+ RAM & Dedicated GPU',
      trustTag: 'No-Cost EMI Available'
    },
    {
      title: 'Top Rated Python & AI Machine Learning Mastery Programs',
      category: 'AI & Dev Certifications',
      badge: '⭐ 4.8 Rating',
      discount: 'Starting ₹499 (Sale Price)',
      merchant: 'Udemy',
      affUrl: `https://www.amazon.in/s?k=python+ai+data+science+books&tag=${AMAZON_TAG}`,
      icon: 'sparkles',
      priceNote: 'Certificate Included',
      trustTag: 'Lifetime Access'
    }
  ],

  // 8. Food & Daily Loot (Swiggy / Zomato / Grocery)
  'food': [
    {
      title: 'Smart Digital Air Fryer & Multi-Cooker Kitchen Gadgets',
      category: 'Kitchen Essentials',
      badge: '🍳 55% OFF',
      discount: 'Save 90% Oil in Cooking',
      merchant: 'Amazon',
      affUrl: `https://www.amazon.in/s?k=air+fryer+digital+4l&tag=${AMAZON_TAG}`,
      icon: 'utensils',
      priceNote: 'Healthy Food at Home',
      trustTag: '2-Year Warranty'
    },
    {
      title: 'Today Food Loot: Swiggy & Zomato Verified Promo Codes & Cashback',
      category: 'Food Delivery Loot',
      badge: '🔥 Flat 60% Off Code',
      discount: 'On Orders Above ₹199',
      merchant: 'Swiggy / Zomato',
      affUrl: `https://www.amazon.in/s?k=gourmet+chocolates+snacks+offers&tag=${AMAZON_TAG}`,
      icon: 'utensils',
      priceNote: 'Auto-Refreshed Daily',
      trustTag: 'Verified Working Codes'
    }
  ]
};

export function getContextualDeals(nicheSlug: string): ContextualDeal[] {
  return NICHE_DEAL_MATRIX[nicheSlug] || NICHE_DEAL_MATRIX['fashion'] || [];
}
