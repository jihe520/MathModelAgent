import type { OutputItem } from "./response";

/** 代码单元格类型 */
export interface CodeCell {
	type: "code";
	content: string;
}

/** 结果单元格类型 */
export interface ResultCell {
	type: "result";
	code_results: OutputItem[];
}

/** 笔记本单元格类型（代码或结果） */
export type NoteCell = CodeCell | ResultCell;

/** 模型配置 */
export interface ModelConfig {
	apiKey: string;
	baseUrl: string;
	modelId: string;
	provider: string;
}
