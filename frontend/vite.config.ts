import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // En desarrollo, /api se reenvía a Django: el navegador ve un solo origen
    // y la cookie del refresh token funciona sin configurar CORS.
    proxy: {
      '/api': 'http://127.0.0.1:8000',
    },
  },
})
