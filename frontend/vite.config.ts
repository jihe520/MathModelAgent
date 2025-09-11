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
		// 开发环境配置 - 直接访问后端，不使用/api代理
		server: {
			// 移除/api代理，开发模式下直接访问localhost:8000
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
