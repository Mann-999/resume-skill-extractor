import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/upload': 'http://localhost:5000',
      '/rewrite-bullets': 'http://localhost:5000',
      '/match-jds': 'http://localhost:5000',
      '/generate-report': 'http://localhost:5000',
    }
  }
})