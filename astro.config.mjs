import { defineConfig } from 'astro/config';

export default defineConfig({
    site: 'https://jmuslu.github.io/personalweb',
    outDir: './dist',
    output: 'static',
    build: {
        assets: '_assets'
    }
});