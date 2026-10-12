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
      title: 'Amazon Lightning Deals: Electronics, Laptops & Smart Gadgets Under ₹9,999',
      category: 'Electronics Loot',
      badge: '🔥 60% OFF',
      discount: 'Additional Bank Discount',
      merchant: 'Amazon',
      affUrl: `https://www.amazon.in/s?k=lightning+deals+electronics&tag=${AMAZON_TAG}`,
      icon: 'sparkles',
      priceNote: 'Limited Stock Offers',
      trustTag: 'Prime Fast Delivery'
    },
    {
      title: 'Quick Commerce Flash Deals: Blinkit & Zepto 10-Minute Grocery & Tech Loot',
      category: '10-Min Flash Delivery',
      badge: '⚡ Flat 50% Off Code',
      discount: 'Instant ₹100 Cashback',
      merchant: 'Blinkit / Zepto / Instamart',
      affUrl: `https://www.amazon.in/s?k=daily+grocery+household+deals&tag=${AMAZON_TAG}`,
      icon: 'tag',
      priceNote: 'Live in Top 20 Indian Cities',
      trustTag: 'Live Today'
    }
  ],

  // Viral & General News
  'viral': [
    {
      title: 'Trending Smart Home Appliances: Inverter ACs, Air Purifiers & Climate Gear',
      category: 'Home & Climate Gear',
      badge: '⚡ Up to 50% Off',
      discount: 'Exchange Bonus + Bank Discount',
      merchant: 'Amazon',
      affUrl: `https://www.amazon.in/s?k=inverter+ac+air+purifier&tag=${AMAZON_TAG}`,
      icon: 'sparkles',
      priceNote: 'Top Rated Inverter Models',
      trustTag: 'Brand Indian Warranty'
    },
    {
      title: 'High-Capacity 20,000mAh Power Banks & 65W GaN Fast Chargers',
      category: 'Everyday Tech Essentials',
      badge: '🔥 Under ₹1,499 Loot',
      discount: 'Flat 55% Off',
      merchant: 'Amazon',
      affUrl: `https://www.amazon.in/s?k=power+bank+20000mah+fast+charging&tag=${AMAZON_TAG}`,
      icon: 'tag',
      priceNote: 'Safe Multi-Device Fast Charge',
      trustTag: 'Amazon Choice'
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
      priceNote: 'Trusted Sellers Only',
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

  // 2. Health & Wellness
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
      title: 'Smart Fitness Trackers, Heart Rate & SpO2 Smartwatches',
      category: 'Health Tech',
      badge: '⚡ Under ₹1,999',
      discount: 'Up to 65% Off',
      merchant: 'Amazon',
      affUrl: `https://www.amazon.in/s?k=smartwatch+fitness+tracker+spo2&tag=${AMAZON_TAG}`,
      icon: 'sparkles',
      priceNote: 'Precise Sleep & Step Count',
      trustTag: 'Official Warranty'
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

  // 5. Fashion & Sneakers Loot
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

  // 6. Cashback & Banking / Credit Cards
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
      trustTag: 'Live Today'
    }
  ],

  // 7. AI Tools & Learning
  'ai-tools': [
    {
      title: 'High-Performance Laptops for AI Coding & Workstations',
      category: 'Workstation Laptops',
      badge: '⚡ Intel Core i7 / M3 Deals',
      discount: 'Up to ₹25,000 Off on Exchange',
      merchant: 'Amazon',
      affUrl: `https://www.amazon.in/s?k=laptop+intel+core+i7+16gb+ram&tag=${AMAZON_TAG}`,
      icon: 'sparkles',
      priceNote: 'Zero Cost EMI Available',
      trustTag: 'Authorized Brand Resellers'
    },
    {
      title: 'Mechanical Keyboards & Ergonomic Wireless Mice for Devs',
      category: 'Coding Setup',
      badge: '🔥 40% OFF',
      discount: 'Under ₹2,499 Deals',
      merchant: 'Amazon',
      affUrl: `https://www.amazon.in/s?k=mechanical+keyboard+wireless+mouse&tag=${AMAZON_TAG}`,
      icon: 'cpu',
      priceNote: 'Hot-Swappable Switches',
      trustTag: '1-Year Warranty'
    }
  ],

  // 8. Food & Grocery Loot
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
      title: 'Today Food Loot: Swiggy & Zomato Promo Codes & Cashback',
      category: 'Food Delivery Loot',
      badge: '🔥 Flat 60% Off Code',
      discount: 'On Orders Above ₹199',
      merchant: 'Swiggy / Zomato',
      affUrl: `https://www.amazon.in/s?k=gourmet+chocolates+snacks+offers&tag=${AMAZON_TAG}`,
      icon: 'utensils',
      priceNote: 'Auto-Refreshed Daily',
      trustTag: 'Working Codes'
    }
  ],

  // 9. Exams, Sarkari Results & Education Hub
  'exams-results': [
    {
      title: 'NCERT Solution Guides, Previous Year Solved Papers & Mock Test Combos',
      category: 'Exam Prep Books',
      badge: '📚 40% OFF',
      discount: 'Latest 2026 Syllabus Editions',
      merchant: 'Amazon',
      affUrl: `https://www.amazon.in/s?k=ncert+solutions+previous+year+solved+papers&tag=${AMAZON_TAG}`,
      icon: 'book-open',
      priceNote: 'Amazon Fast Prime Delivery',
      trustTag: '100% Original Publisher'
    },
    {
      title: 'Study Tablets with Stylus & Digital Note-Taking Gadgets (iPad / Galaxy Tab)',
      category: 'Digital Study Tech',
      badge: '⚡ Up to ₹8,000 Off',
      discount: 'No-Cost EMI from ₹1,200/mo',
      merchant: 'Amazon',
      affUrl: `https://www.amazon.in/s?k=study+tablets+with+stylus+pen&tag=${AMAZON_TAG}`,
      icon: 'sparkles',
      priceNote: 'Eye-Comfort Display for PDF Prep',
      trustTag: 'Official Brand Warranty'
    }
  ]
};

/**
 * Intelligent context-aware deal matcher.
 * Matches article title & summary first, then niche category, falling back cleanly to top deals.
 */
export function getContextualDeals(nicheSlug: string, postTitle?: string, postSummary?: string): ContextualDeal[] {
  const combinedText = `${postTitle || ''} ${postSummary || ''}`.toLowerCase();

  // 1. Weather / Climate / Cooling / Air Quality Intent Matcher
  if (/cooling|air purifier|purifier|hepa|ac\b|conditioner|heatwave|weather|smog|pollution|winter|summer|delhi weather|aqi/i.test(combinedText)) {
    return [
      {
        title: 'Smart Inverter Split ACs (1.5 Ton 5-Star Energy Saver)',
        category: 'Cooling Appliances',
        badge: '⚡ Up to 45% Off',
        discount: 'Free Installation + Instant Bank Off',
        merchant: 'Amazon',
        affUrl: `https://www.amazon.in/s?k=1.5+ton+5+star+inverter+split+ac&tag=${AMAZON_TAG}`,
        icon: 'sparkles',
        priceNote: 'Copper Condenser • Smart WiFi',
        trustTag: 'Official Brand Warranty'
      },
      {
        title: 'True HEPA Air Purifiers with Real-Time AQI & PM2.5 Display',
        category: 'Air Quality & Health',
        badge: '🔥 Bestseller',
        discount: 'Flat 40% Off',
        merchant: 'Amazon',
        affUrl: `https://www.amazon.in/s?k=true+hepa+air+purifier+pm2.5&tag=${AMAZON_TAG}`,
        icon: 'sparkles',
        priceNote: 'Removes 99.97% Smoke & Pollutants',
        trustTag: 'Doctor Recommended'
      }
    ];
  }

  // 2. Cricket / Live Sports Intent Matcher
  if (/cricket|ipl|t20|world cup|match|stadium|bcci|scorecard|wicket|batsman/i.test(combinedText)) {
    return [
      {
        title: '4K Ultra HD Smart TV & Stadium Soundbar Bundles',
        category: 'Live Match Viewing',
        badge: '🏏 Match Day Loot',
        discount: 'Up to 55% Off',
        merchant: 'Amazon',
        affUrl: `https://www.amazon.in/s?k=55+inch+4k+smart+tv+soundbar&tag=${AMAZON_TAG}`,
        icon: 'clapperboard',
        priceNote: 'Dolby Vision • 120Hz Refresh',
        trustTag: '100% Genuine Warranty'
      },
      {
        title: 'Official Team India Supporter Jersey & Grade English Willow Bat',
        category: 'Cricket Merchandise',
        badge: '⚡ Fan Choice',
        discount: 'Starting ₹499',
        merchant: 'Amazon',
        affUrl: `https://www.amazon.in/s?k=cricket+jersey+bat+kit&tag=${AMAZON_TAG}`,
        icon: 'sparkles',
        priceNote: 'Breathable Dry-Fit Fabric',
        trustTag: 'Prime Delivery'
      }
    ];
  }

  // 3. Smartphone / Mobile Intent Matcher
  if (/phone|smartphone|5g|iphone|oneplus|samsung|pixel|snapdragon|charger/i.test(combinedText)) {
    return [
      {
        title: 'Latest 5G Smartphones & Bank Exchange Bonuses',
        category: 'Mobile Deals',
        badge: '🔥 Live Drop',
        discount: 'Up to ₹10,000 Off on Exchange',
        merchant: 'Amazon',
        affUrl: `https://www.amazon.in/s?k=5g+smartphone+deals&tag=${AMAZON_TAG}`,
        icon: 'sparkles',
        priceNote: 'No-Cost EMI Available',
        trustTag: 'Official Brand Warranty'
      },
      {
        title: '65W GaN Multi-Port Fast Charger & Braided Cable Combo',
        category: 'Charging Gear',
        badge: '⚡ Under ₹999 Loot',
        discount: 'Flat 50% Off',
        merchant: 'Amazon',
        affUrl: `https://www.amazon.in/s?k=65w+gan+charger+type+c&tag=${AMAZON_TAG}`,
        icon: 'tag',
        priceNote: 'Charges Laptop, Phone & Tablet',
        trustTag: 'Tested & Certified'
      }
    ];
  }

  // 4. Exact Niche slug fallback
  if (NICHE_DEAL_MATRIX[nicheSlug]) {
    return NICHE_DEAL_MATRIX[nicheSlug];
  }

  // 5. Universal high-converting tech/deals fallback (NEVER irrelevant fashion sneakers)
  return NICHE_DEAL_MATRIX['deals'];
}
