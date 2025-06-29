// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import * as path from 'path';   // ← 이렇게 바꿔 보세요

export default defineConfig({
  plugins: [react(),
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
    
  },
  server: {
  host: '0.0.0.0',
  port: 3000,  // nginx랑 충돌 안 나게 조심
  
}
});
