import { getTaskMessages } from "@/apis/commonApi";
import { AgentType } from "@/utils/enum";
import type {
	CoderMessage,
	CoordinatorMessage,
	InterpreterMessage,
	Message,
	ModelerMessage,
	UserMessage,
	WriterMessage,
} from "@/utils/response";
import { TaskWebSocket } from "@/utils/websocket";
import { defineStore } from "pinia";
import { computed, ref } from "vue";

/** 任务管理 Store */
export const useTaskStore = defineStore("task", () => {
	// ---- State ----

	/** 按任务ID分组的消息记录 */
	const messagesByTask = ref<Record<string, Message[]>>({});

	/** 当前活跃的任务ID */
	const currentTaskId = ref<string | null>(null);

	/** 当前任务的消息列表（计算属性） */
	const messages = computed<Message[]>(() => {
		if (!currentTaskId.value) {
			return [];
		}
		return messagesByTask.value[currentTaskId.value] ?? [];
	});
	/** 已处理的消息ID集合（用于去重） */
	const seenMessageIdsByTask = new Map<string, Set<string>>();

	/** WebSocket 实例 */
	let ws: TaskWebSocket | null = null;

	/** WebSocket 连接状态 */
	const wsStatus = ref<
		"connecting" | "connected" | "disconnected" | "reconnecting"
	>("disconnected");

	// ---- Helpers ----

	/** 获取消息时间戳 */
	function getMessageTimestamp(message: Message): number | null {
		if (!message.created_at) {
			return null;
		}
		const timestamp = Date.parse(message.created_at);
		return Number.isNaN(timestamp) ? null : timestamp;
	}

	/** 按时间戳排序消息 */
	function sortMessages(items: Message[]) {
		return [...items].sort((left, right) => {
			const leftTs = getMessageTimestamp(left);
			const rightTs = getMessageTimestamp(right);
			if (leftTs == null || rightTs == null || leftTs === rightTs) {
				return 0;
			}
			return leftTs - rightTs;
		});
	}

	/** 类型守卫：判断是否为有效的消息对象 */
	function isMessagePayload(payload: unknown): payload is Message {
		if (!payload || typeof payload !== "object") {
			return false;
		}
		const msgType = Reflect.get(payload, "msg_type");
		return (
			typeof Reflect.get(payload, "id") === "string" &&
			typeof msgType === "string" &&
			["system", "agent", "user", "tool"].includes(msgType)
		);
	}

	/** 设置当前活跃任务 */
	function setCurrentTask(taskId: string) {
		currentTaskId.value = taskId;
		if (typeof window !== "undefined") {
			window.localStorage.setItem("currentTaskId", taskId);
		}
	}

	/** 确保任务的消息桶存在 */
	function ensureTaskBucket(taskId: string) {
		if (!messagesByTask.value[taskId]) {
			messagesByTask.value[taskId] = [];
		}
		if (!seenMessageIdsByTask.has(taskId)) {
			seenMessageIdsByTask.set(taskId, new Set());
		}
	}

	/** 追加消息（自动去重和排序） */
	function appendMessage(taskId: string, message: Message) {
		ensureTaskBucket(taskId);
		const seenIds = seenMessageIdsByTask.get(taskId);
		if (message.id && seenIds?.has(message.id)) {
			messagesByTask.value[taskId] = sortMessages(
				messagesByTask.value[taskId].map((existing) =>
					existing.id === message.id ? message : existing,
				),
			);
			return;
		}
		if (message.id) {
			seenIds?.add(message.id);
		}
		messagesByTask.value[taskId] = sortMessages([
			...messagesByTask.value[taskId],
			message,
		]);
	}

	/** 合并历史消息（用于加载历史记录） */
	function mergeMessages(taskId: string, incomingMessages: Message[]) {
		ensureTaskBucket(taskId);
		const existingMessages = messagesByTask.value[taskId];
		const mergedById = new Map<string, Message>();

		for (const message of [...existingMessages, ...incomingMessages]) {
			if (!message.id) {
				continue;
			}
			mergedById.set(message.id, message);
		}

		const mergedMessages = Array.from(mergedById.values());
		messagesByTask.value[taskId] = sortMessages(mergedMessages);
		seenMessageIdsByTask.set(
			taskId,
			new Set(mergedMessages.map((message) => message.id)),
		);
	}

	// ---- Actions ----

	/** 连接 WebSocket 接收实时消息 */
	function connectWebSocket(taskId: string) {
		if (ws) {
			ws.close();
			ws = null;
		}
		setCurrentTask(taskId);
		ensureTaskBucket(taskId);

		const baseUrl = import.meta.env.VITE_WS_URL;
		const wsUrl = `${baseUrl}/task/${taskId}`;

		ws = new TaskWebSocket(
			wsUrl,
			(data) => {
				if (!isMessagePayload(data)) {
					console.warn("忽略非标准任务消息:", data);
					return;
				}
				appendMessage(taskId, data);
			},
			(status) => {
				wsStatus.value = status;
			},
		);
		// 初始化测试数据（已在上面初始化，这里可以注释掉）
		// messages.value = messageData as Message[]
		ws.connect();
	}

	/** 加载任务的历史消息 */
	async function loadTaskMessages(taskId: string) {
		setCurrentTask(taskId);
		ensureTaskBucket(taskId);
		try {
			const response = await getTaskMessages(taskId);
			const validMessages = (response.data ?? []).filter(isMessagePayload);
			mergeMessages(taskId, validMessages);
		} catch (error) {
			console.error("加载任务历史消息失败:", error);
		}
	}

	/** 关闭 WebSocket 连接 */
	function closeWebSocket() {
		ws?.close();
		ws = null;
	}

	/** 添加用户消息 */
	function addUserMessage(content: string) {
		const taskId = currentTaskId.value ?? "local";
		appendMessage(taskId, {
			id: Date.now().toString(),
			msg_type: "user",
			content: content,
		} as UserMessage);
	}

	/** 下载消息为 JSON 文件 */
	function downloadMessages() {
		const dataStr = `data:text/json;charset=utf-8,${encodeURIComponent(JSON.stringify(messages.value, null, 2))}`;
		const downloadAnchorNode = document.createElement("a");
		downloadAnchorNode.setAttribute("href", dataStr);
		downloadAnchorNode.setAttribute(
			"download",
			`${currentTaskId.value ?? "task"}-messages.json`,
		);
		document.body.appendChild(downloadAnchorNode);
		downloadAnchorNode.click();
		downloadAnchorNode.remove();
	}

	// ---- Computed ----

	/** 聊天消息列表（用户、Coder Agent、系统消息） */
	const chatMessages = computed(() =>
		messages.value.filter((msg) => {
			if (
				msg.msg_type === "agent" &&
				msg.agent_type === AgentType.CODER &&
				msg.content != null &&
				msg.content !== ""
			) {
				return true;
			}
			if (msg.msg_type === "user") {
				return true;
			}
			if (msg.msg_type === "system") {
				return true;
			}
			// if (msg.msg_type === 'tool' && msg.tool_name === 'execute_code') {
			// return true
			// }
			return false;
		}),
	);

	/** 协调者消息列表 */
	const coordinatorMessages = computed(() =>
		messages.value.filter(
			(msg): msg is CoordinatorMessage =>
				msg.msg_type === "agent" &&
				msg.agent_type === AgentType.COORDINATOR &&
				msg.content != null,
		),
	);

	/** 建模者消息列表 */
	const modelerMessages = computed(() =>
		messages.value.filter(
			(msg): msg is ModelerMessage =>
				msg.msg_type === "agent" &&
				msg.agent_type === AgentType.MODELER &&
				msg.content != null,
		),
	);

	/** 代码手消息列表 */
	const coderMessages = computed(() =>
		messages.value.filter(
			(msg): msg is CoderMessage =>
				msg.msg_type === "agent" &&
				msg.agent_type === AgentType.CODER &&
				msg.content != null,
		),
	);

	/** 论文手消息列表 */
	const writerMessages = computed(() =>
		messages.value.filter(
			(msg): msg is WriterMessage =>
				msg.msg_type === "agent" &&
				msg.agent_type === AgentType.WRITER &&
				msg.content != null,
		),
	);

	/** 代码执行工具消息列表 */
	const interpreterMessage = computed(() =>
		messages.value.filter(
			(msg): msg is InterpreterMessage =>
				msg.msg_type === "tool" &&
				"tool_name" in msg &&
				msg.tool_name === "execute_code",
		),
	);

	/** 从最新代码手消息中提取文件列表 */
	const files = computed(() => {
		// 反向遍历消息找到最新的文件列表
		for (let i = coderMessages.value.length - 1; i >= 0; i--) {
			const msg = coderMessages.value[i];
			if (
				"files" in msg &&
				msg.files &&
				Array.isArray(msg.files) &&
				msg.files.length > 0
			) {
				console.log("找到文件列表:", msg.files);
				return msg.files;
			}
		}
		// 如果没有找到文件列表，返回空数组
		console.log("没有找到文件列表，返回空数组");
		return [];
	});

	// 初始化连接
	// 如果需要自动连接，可以在这里添加代码
	// 例如：connectWebSocket('default')

	return {
		messages,
		wsStatus,
		chatMessages,
		coordinatorMessages,
		modelerMessages,
		coderMessages,
		writerMessages,
		interpreterMessage,
		files,
		loadTaskMessages,
		connectWebSocket,
		closeWebSocket,
		downloadMessages,
		addUserMessage,
	};
});
