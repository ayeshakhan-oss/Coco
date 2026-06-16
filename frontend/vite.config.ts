import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// Dev server proxies API calls to the FastAPI backend on :8000 so the SPA can
// use same-origin relative URLs (and cookies work without CORS friction).
export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    port: 5173,
    proxy: {
      // Explicit IPv4 — avoids the Windows localhost->::1 mismatch when
      // uvicorn binds to 127.0.0.1.
      '/api': 'http://127.0.0.1:8000',
      '/auth': 'http://127.0.0.1:8000',
      '/healthz': 'http://127.0.0.1:8000',
      '/readyz': 'http://127.0.0.1:8000',
    },
  },
})
