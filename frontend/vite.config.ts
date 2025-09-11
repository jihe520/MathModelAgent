import path from "node:path";
import vue from "@vitejs/plugin-vue";
import autoprefixer from "autoprefixer";
import tailwind from "tailwindcss";
import { defineConfig } from "vite";

export default defineConfig(({ mode }) => {
	return {
		css: {
			postcss: {
				plugins: [tailwind(), autoprefixer()],
			},
		},
		plugins: [vue()],
		resolve: {
			alias: {
				"@": path.resolve(__dirname, "./src"),
			},
		},
		// 开发环境配置
		server: {
			proxy: {
				'/api': {
					target: 'http://localhost:8000',
					changeOrigin: true,
					rewrite: (path) => path.replace(/^\/api/, '')
				},
				'/ws': {
					target: 'ws://localhost:8000',
					ws: true,
					changeOrigin: true
				}
			}
		},
		// 生产环境构建配置
		build: {
			outDir: 'dist',
			assetsDir: 'assets',
			sourcemap: false,
			minify: 'esbuild'
		}
	};
});
