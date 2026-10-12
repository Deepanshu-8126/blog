/**
 * =============================================================================
 * 100% FREE & UNLIMITED TELEGRAM -> WHATSAPP CHANNEL AUTO-POSTER BRIDGE
 * =============================================================================
 * Powered by Baileys (Zero API cost, Zero limits, Permanent self-hosted)
 * 
 * Features:
 *  1. One-time terminal QR code scan (Saved in ./auth_info)
 *  2. Auto-resolves Channel: https://whatsapp.com/channel/0029Vb90gso4dTnKKpcf7M1E
 *  3. Monitors your Telegram channel (@uniquedigit_deals) in real time (every 5s)
 *  4. Direct HTTP API endpoint on http://127.0.0.1:5005/post_deal
 *  5. Posts full formatted cards + HD photos directly into WhatsApp Channel!
 * =============================================================================
 */

import makeWASocket, {
  useMultiFileAuthState,
  DisconnectReason,
  fetchLatestBaileysVersion
} from '@whiskeysockets/baileys';
import qrcode from 'qrcode-terminal';
import pino from 'pino';
import http from 'http';
import fs from 'fs';
import path from 'path';

const CHANNEL_INVITE_CODE = process.env.WHATSAPP_CHANNEL_CODE || '0029Vb90gso4dTnKKpcf7M1E';
const TG_CHANNEL_NAME = process.env.TELEGRAM_CHANNEL_NAME || 'uniquedigit_deals';
const AUTH_DIR = path.resolve('auth_info');
const CACHE_FILE = path.resolve('sent_whatsapp_cache.json');
const HTTP_PORT = 5005;

let waSock = null;
let targetChannelJid = null;

// Persistent cache to ensure 0 duplicate posts to WhatsApp
function loadCache() {
  try {
    if (fs.existsSync(CACHE_FILE)) {
      return JSON.parse(fs.readFileSync(CACHE_FILE, 'utf8'));
    }
  } catch (e) {}
  return {};
}

function saveCache(cache) {
  try {
    fs.writeFileSync(CACHE_FILE, JSON.stringify(cache, null, 2), 'utf8');
  } catch (e) {}
}

const seenCache = loadCache();

async function sendToWhatsAppChannel(text, photoUrl = '') {
  if (!waSock || !targetChannelJid) {
    console.error('❌ WhatsApp socket or Channel JID not ready yet!');
    return false;
  }

  try {
    if (photoUrl && photoUrl.startsWith('http')) {
      console.log(`📸 Sending HD photo deal to WhatsApp Channel...`);
      await waSock.sendMessage(targetChannelJid, {
        image: { url: photoUrl },
        caption: text
      });
    } else {
      console.log(`💬 Sending text deal to WhatsApp Channel...`);
      await waSock.sendMessage(targetChannelJid, { text });
    }
    console.log(`✅ Deal posted to WhatsApp Channel successfully!`);
    return true;
  } catch (err) {
    console.error(`❌ Failed to send deal to WhatsApp Channel:`, err.message);
    return false;
  }
}

// Telegram Channel Spy (Grabs latest posts from @uniquedigit_deals)
function formatForWhatsApp(rawHtml, wrapHtml) {
  // 1. Extract all outbound links in the message wrap (including inline buttons)
  const linkMatches = [...wrapHtml.matchAll(/href="([^"]+)"/g)].map(m => m[1]);
  const storeLink = linkMatches.find(l => 
    l.includes('amazon.in') || 
    l.includes('meesho.com') || 
    l.includes('flipkart.com') || 
    l.includes('myntra.com') || 
    l.includes('earnkaro.com') || 
    l.includes('ajio.com')
  ) || linkMatches.find(l => !l.includes('t.me') && !l.includes('vault') && !l.includes('whatsapp.com'));

  // 2. Convert HTML tags to native WhatsApp markdown (*bold*, ~strike~, _italics_)
  let waText = rawHtml
    .replace(/<br\s*\/?>/gi, '\n')
    .replace(/<b>(.*?)<\/b>/gi, '*$1*')
    .replace(/<strong>(.*?)<\/strong>/gi, '*$1*')
    .replace(/<s>(.*?)<\/s>/gi, '~$1~')
    .replace(/<strike>(.*?)<\/strike>/gi, '~$1~')
    .replace(/<i>(.*?)<\/i>/gi, '_$1_')
    .replace(/<em>(.*?)<\/em>/gi, '_$1_')
    .replace(/<a [^>]*href="([^"]+)"[^>]*>([\s\S]*?)<\/a>/gi, '$2: $1')
    .replace(/<[^>]+>/g, '')
    // Clean up any Telegram button instructions
    .replace(/1\.\s*Tap\s*['"]?GRAB LOOT DEAL['"]?[^\n]*/gi, '')
    .replace(/✂️\s*\*?HOW TO CLAIM LOOT:\*?/gi, '')
    .replace(/2\.\s*Apply store coupon[^\n]*/gi, '')
    .replace(/3\.\s*Order fast[^\n]*/gi, '')
    .trim();

  // 3. Inject prominent direct clickable WhatsApp buy link if not already present
  if (storeLink && !waText.includes(storeLink)) {
    waText += `\n\n🛒 *ORDER LOOT DEAL HERE:*\n👉 ${storeLink}`;
  }

  // 4. Clean consecutive empty newlines
  waText = waText.replace(/\n{3,}/g, '\n\n');

  if (!waText.includes('🚨') && !waText.includes('⏰') && !waText.includes('🔥') && !waText.includes('⚡')) {
    waText += `\n\n🚨 _Fast Loot! Order fast before price changes or stock ends!_`;
  }
  return waText;
}

// Telegram Channel Spy (Grabs latest posts from @uniquedigit_deals and dynamic-formats for WhatsApp)
async function checkTelegramChannel() {
  try {
    const url = `https://t.me/s/${TG_CHANNEL_NAME}`;
    const res = await fetch(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
      }
    });
    if (!res.ok) return;
    const html = await res.text();

    const msgWraps = [...html.matchAll(/<div class="tgme_widget_message_wrap[^>]*>([\s\S]*?)<\/div>\s*<\/div>\s*<\/div>/g)];
    
    // Check last 3 messages
    for (const wrapMatch of msgWraps.slice(-3)) {
      const wrapHtml = wrapMatch[1];
      
      const postMatch = wrapHtml.match(/data-post="([^"]+)"/);
      if (!postMatch) continue;
      const postId = postMatch[1];

      if (seenCache[postId]) continue; // Already posted to WhatsApp

      // Extract text HTML
      const textMatch = wrapHtml.match(/<div class="tgme_widget_message_text[^>]*>([\s\S]*?)<\/div>/);
      if (!textMatch) continue;

      const dynamicWhatsAppText = formatForWhatsApp(textMatch[1], wrapHtml);

      // Extract photo
      let photoUrl = '';
      const photoMatch = wrapHtml.match(/background-image:url\('([^']+)'\)/);
      if (photoMatch) {
        photoUrl = photoMatch[1];
      }

      console.log(`\n⚡ Dynamic WhatsApp deal detected from @${TG_CHANNEL_NAME} [${postId}]`);
      const success = await sendToWhatsAppChannel(dynamicWhatsAppText, photoUrl);
      if (success) {
        seenCache[postId] = { time: new Date().toISOString() };
        saveCache(seenCache);
      }
    }
  } catch (err) {
    // Non-fatal, retry next cycle
  }
}

// Start HTTP Server for instant direct deal pushing from Python
function startHttpServer() {
  const server = http.createServer(async (req, res) => {
    if (req.method === 'POST' && req.url === '/post_deal') {
      let body = '';
      req.on('data', chunk => { body += chunk.toString(); });
      req.on('end', async () => {
        try {
          const payload = JSON.parse(body);
          const ok = await sendToWhatsAppChannel(payload.text, payload.photo_url || '');
          res.writeHead(ok ? 200 : 500, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ success: ok }));
        } catch (e) {
          res.writeHead(400, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: e.message }));
        }
      });
    } else {
      res.writeHead(200, { 'Content-Type': 'text/plain' });
      res.end('UniqueDigit WhatsApp Channel Bridge is Running!');
    }
  });

  server.listen(HTTP_PORT, '127.0.0.1', () => {
    console.log(`🌐 Local HTTP API listening on http://127.0.0.1:${HTTP_PORT}/post_deal`);
  });
}

// Connect to WhatsApp Web
async function startWhatsApp() {
  console.log('🔄 Initializing WhatsApp Web Connection...');
  const { state, saveCreds } = await useMultiFileAuthState(AUTH_DIR);
  const { version } = await fetchLatestBaileysVersion();

  waSock = makeWASocket({
    version,
    logger: pino({ level: 'silent' }),
    auth: state,
    printQRInTerminal: false,
    browser: ['UniqueDigit Deals', 'Chrome', '124.0.0']
  });

  waSock.ev.on('creds.update', saveCreds);

  waSock.ev.on('connection.update', async (update) => {
    const { connection, lastDisconnect, qr } = update;

    if (qr) {
      console.log('\n======================================================');
      console.log('📱 SCAN THIS QR CODE WITH YOUR WHATSAPP TO CONNECT:');
      console.log('👉 WhatsApp -> Settings / 3-Dots -> Linked Devices -> Link a Device');
      console.log('======================================================\n');
      qrcode.generate(qr, { small: true });
    }

    if (connection === 'close') {
      const shouldReconnect = (lastDisconnect?.error)?.output?.statusCode !== DisconnectReason.loggedOut;
      console.log(`⚠️ Connection closed. Reconnecting: ${shouldReconnect}...`);
      if (shouldReconnect) {
        setTimeout(startWhatsApp, 3000);
      }
    } else if (connection === 'open') {
      console.log('\n🎉 ===================================================');
      console.log('✅ WHATSAPP CONNECTED SUCCESSFULLY!');
      console.log('=====================================================\n');

      // Resolve Newsletter Channel
      try {
        console.log(`🔍 Resolving Channel ID for invite code: ${CHANNEL_INVITE_CODE}...`);
        const metadata = await waSock.newsletterMetadata('invite', CHANNEL_INVITE_CODE);
        targetChannelJid = metadata.id;
        console.log(`📢 Channel Found: "${metadata.name}" (ID: ${targetChannelJid})`);
        console.log(`🚀 Ready to post 100% Free & Unlimited deals to WhatsApp Channel!`);
      } catch (err) {
        console.warn(`⚠️ Could not auto-resolve channel via invite code (${err.message}). Listening for incoming updates...`);
      }

      // Start continuous Telegram monitoring loop every 5 seconds
      setInterval(checkTelegramChannel, 5000);
      checkTelegramChannel();
    }
  });
}

startHttpServer();
startWhatsApp();
