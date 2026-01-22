import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import path from "path";
import { componentTagger } from "lovable-tagger";

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => ({
  server: {
    host: '0.0.0.0',
    port: 5173,
    watch: {
      usePolling: true
    },
    // --- CONFIGURAÇÃO DE PROXY ---
    // Redireciona as chamadas do frontend para o Nginx (porta 80)
    proxy: {
      '/api': {
        target: 'http://localhost:80', // Endereço do Nginx
        changeOrigin: true,
        secure: false,
      },
      '/hls': {
        target: 'http://localhost:80', // Streaming via Nginx
        changeOrigin: true,
        secure: false,
      },
      '/stream-ctl': {
        target: 'http://localhost:80', // Gateway via Nginx
        changeOrigin: true,
        secure: false,
      }
    }
  },
  plugins: [react(), mode === "development" && componentTagger()].filter(Boolean),
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
}));