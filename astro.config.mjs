import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

// Configuração estática com trailingSlash para compatibilidade com Vercel
export default defineConfig({
  integrations: [tailwind()],
  trailingSlash: 'always',
  build: {
    inlineStylesheets: 'always'
  }
});
