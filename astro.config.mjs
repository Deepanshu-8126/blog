import { defineConfig } from 'astro/config';
import cloudflare from '@astrojs/cloudflare';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  site: 'https://uniquedigit-viral-hub.pages.dev',
  output: 'server',
  adapter: cloudflare({
    imageService: 'passthrough'
  }),
  integrations: [
    tailwind({
      applyBaseStyles: false
    })
  ]
});
