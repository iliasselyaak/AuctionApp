import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
  ],
  build : {
    emptyOutDir:true,
    outDir: '../static/auctionapp/vue'
  }
})
