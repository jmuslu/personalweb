import { defineConfig } from 'astro/config';

export default defineConfig({
    site: 'https://jmuslu.github.io',

    outDir: './dist',
    output: 'static',
    build: {
        assets: '_assets'
    }
});