/** 对应后端 response.py 的消息结构定义 */

import type { AgentType } from "./enum";

/** 系统消息类型 */
export type SystemMessageType = "info" | "warning" | "success" | "error";

/** 消息基础接口 */
export interface BaseMessage {
	id: string;
	created_at?: string;
	msg_type: "system" | "agent" | "user" | "tool";
	content?: string | null;
}

/** 工具调用消息 */
export interface ToolMessage extends BaseMessage {
	msg_type: "tool";
	tool_name: "execute_code" | "search_scholar";
	input: Record<string, unknown> | null;
	output: string[] | OutputItem[] | null;
}

/** 系统通知消息 */
export interface SystemMessage extends BaseMessage {
	msg_type: "system";
	type: SystemMessageType;
}

/** 用户消息 */
export interface UserMessage extends BaseMessage {
	msg_type: "user";
}

/** Agent 消息基类 */
export interface AgentMessage extends BaseMessage {
	msg_type: "agent";
	agent_type: AgentType;
}

/** 建模手消息 */
export interface ModelerMessage extends AgentMessage {
	agent_type: AgentType.MODELER;
}

/** 协调者消息 */
export interface CoordinatorMessage extends AgentMessage {
	agent_type: AgentType.COORDINATOR;
}

/** 代码执行结果格式类型 */
export type ExecutionFormat =
	| "text"
	| "html"
	| "markdown"
	| "png"
	| "jpeg"
	| "svg"
	| "pdf"
	| "latex"
	| "json"
	| "javascript";

/** 代码执行结果基类 */
export interface BaseCodeExecution {
	res_type: "stdout" | "stderr" | "result" | "error";
	msg?: string;
}

/** 标准输出执行结果 */
export interface StdOutExecution extends BaseCodeExecution {
	res_type: "stdout";
}

/** 标准错误执行结果 */
export interface StdErrExecution extends BaseCodeExecution {
	res_type: "stderr";
}

/** 执行结果 */
export interface ResultExecution extends BaseCodeExecution {
	res_type: "result";
	format: ExecutionFormat;
}

/** 执行错误 */
export interface ErrorExecution extends BaseCodeExecution {
	res_type: "error";
	name: string;
	value: string;
	traceback: string;
}

/** 代码执行输出项 */
export type OutputItem =
	| StdOutExecution
	| StdErrExecution
	| ResultExecution
	| ErrorExecution;

/** 文献搜索工具消息 */
export interface ScholarMessage extends ToolMessage {
	tool_name: "search_scholar";
	input: Record<string, never>;
	output: string[];
}

/** 代码执行工具消息 */
export interface InterpreterMessage extends ToolMessage {
	tool_name: "execute_code";
	input: {
		code: string;
	} | null;
	output: OutputItem[] | null;
}

/** 代码手消息 */
export interface CoderMessage extends AgentMessage {
	agent_type: AgentType.CODER;
}

/** 论文手消息 */
export interface WriterMessage extends AgentMessage {
	agent_type: AgentType.WRITER;
	sub_title?: string;
}

/** 所有消息类型的联合类型 */
export type Message =
	| SystemMessage
	| UserMessage
	| CoderMessage
	| WriterMessage
	| ModelerMessage
	| CoordinatorMessage
	| ToolMessage;
