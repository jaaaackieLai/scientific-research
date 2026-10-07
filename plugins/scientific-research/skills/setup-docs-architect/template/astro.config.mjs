import { defineConfig } from 'astro/config';

// Output as dist/<page>.html with CSS inlined, so a single page can be opened directly.
export default defineConfig({
  build: {
    format: 'file',
    inlineStylesheets: 'always',
  },
});
