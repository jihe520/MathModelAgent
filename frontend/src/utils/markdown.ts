import katex from "katex";
import { marked } from "marked";
import type { Renderer, RendererObject, Token } from "marked";

// 默认的markdown渲染配置
const defaultOptions = {
	breaks: true, // 允许换行
	gfm: true, // 启用GitHub风格的Markdown
	headerIds: true, // 为标题添加id
	mangle: false, // 不转义标题中的HTML
	sanitize: false, // 不净化HTML
};

// 处理数学公式
const renderMath = (tex: string, displayMode = false) => {
	try {
		return katex.renderToString(tex, {
			displayMode: displayMode,
			throwOnError: false,
			strict: false,
		});
	} catch (err) {
		console.error("KaTeX rendering error:", err);
		return tex;
	}
};

// 创建自定义渲染器
const renderer: Partial<RendererObject> = {
	paragraph(this: Renderer, token: { text: string }) {
		let text = token.text;

		// 先处理图片链接，避免被误识别为数学公式
		const imagePattern = /!\[(.*?)\]\((.*?)\)/g;
		const images: Array<[string, string, string]> = [];
		let imageIndex = 0;
		text = text.replace(imagePattern, (match, alt, src) => {
			images.push([match, alt, src]);
			return `__IMAGE_PLACEHOLDER_${imageIndex++}__`;
		});

		// 处理块级公式（使用 $$ 包裹）
		const blockMathPattern = /\$\$([\s\S]*?)\$\$/g;
		text = text.replace(blockMathPattern, (_, tex) => {
			return `<div class="math-block">${renderMath(tex.trim(), true)}</div>`;
		});

		// 处理行内公式（使用 \( \) 包裹）
		text = text.replace(/\\\((.*?)\\\)/g, (_, tex) =>
			renderMath(tex.trim(), false),
		);

		// 还原图片占位符
		text = text.replace(/__IMAGE_PLACEHOLDER_(\d+)__/g, (_, index) => {
			const [, alt, src] = images[Number.parseInt(index)];
			return `<img src="${src}" alt="${alt}" class="max-w-full h-auto" />`;
		});

		return `<p>${text}</p>`;
	},
};

// 配置marked
marked.use({ renderer });

// 配置图片处理
marked.use({
	hooks: {
		preprocess(markdown) {
			// 处理图片链接
			const baseUrl =
				import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
			const taskId = window.localStorage.getItem("currentTaskId") || "";

			return markdown.replace(
				/!\[(.*?)\]\(((?!http[s]?:\/\/).*?\.(?:png|jpg|jpeg|gif|bmp|webp))\)/g,
				(_, alt, src) => `![${alt}](${baseUrl}/static/${taskId}/${src})`,
			);
		},
	},
});

/**
 * 渲染Markdown文本为HTML
 * @param content Markdown文本
 * @param options 可选的marked配置项
 * @returns 渲染后的HTML
 */
export const renderMarkdown = async (content: string, options = {}) => {
	// 预处理内容，确保数学公式正确换行
	const normalized = content
		.replace(/\\\[\s*\n/g, "\\[")
		.replace(/\n\s*\\\]/g, "\\]");
	return marked.parse(normalized, { ...defaultOptions, ...options });
};

/**
 * 计算Markdown文本的行数
 * @param content Markdown文本
 * @returns 行数
 */
export const getMarkdownLines = (content: string) => {
	return content.split("\n").length;
};

// 导出marked以备需要直接使用
export { marked };
