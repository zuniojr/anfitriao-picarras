import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

// Alterado para saída estática (padrão) para melhor performance e compatibilidade com Vercel
export default defineConfig({
  integrations: [tailwind()],
});
