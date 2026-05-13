/** Agent 类型枚举 */
export enum AgentType {
	COORDINATOR = "CoordinatorAgent",
	MODELER = "ModelerAgent",
	CODER = "CoderAgent",
	WRITER = "WriterAgent",
}

/** LLM API 类型枚举 */
export enum ApiType {
	OPENAI_CHAT = "openai-chat",
	OPENAI_RESPONSES = "openai-responses",
	ANTHROPIC = "anthropic",
}
