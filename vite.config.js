import { resolve } from 'node:path';
import { defineConfig } from 'vite';

// Multi-page build: each page is its own HTML entry.
export default defineConfig({
  build: {
    rollupOptions: {
      input: {
        main: resolve(import.meta.dirname, 'index.html'),
        cabin: resolve(import.meta.dirname, 'cabin/index.html'),
        gallery: resolve(import.meta.dirname, 'gallery/index.html'),
        reviews: resolve(import.meta.dirname, 'reviews/index.html'),
      },
    },
  },
});
