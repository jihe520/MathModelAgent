/** WebSocket 消息处理回调函数类型 */
type MessageHandler = (data: unknown) => void;

/** 连接状态变化回调函数类型 */
type StatusHandler = (
	status: "connecting" | "connected" | "disconnected" | "reconnecting",
) => void;

/** 重连配置 */
interface ReconnectConfig {
	/** 最大重试次数 */
	maxRetries: number;
	/** 初始重试延迟（毫秒） */
	initialDelay: number;
	/** 最大重试延迟（毫秒） */
	maxDelay: number;
}

/** 任务 WebSocket 连接管理类 */
export class TaskWebSocket {
	private socket: WebSocket | null = null;
	private url: string;
	private onMessage: MessageHandler;
	private onStatus: StatusHandler | null = null;
	private reconnectConfig: ReconnectConfig;
	private reconnectAttempts = 0;
	private reconnectTimer: ReturnType<typeof setTimeout> | null = null;
	private isManualClose = false;

	constructor(
		url: string,
		onMessage: MessageHandler,
		onStatus?: StatusHandler,
	) {
		this.url = url;
		this.onMessage = onMessage;
		this.onStatus = onStatus ?? null;
		this.reconnectConfig = {
			maxRetries: 10,
			initialDelay: 1000,
			maxDelay: 30000,
		};
	}

	/** 建立 WebSocket 连接 */
	connect() {
		this.isManualClose = false;
		this.notifyStatus("connecting");

		this.socket = new WebSocket(this.url);
		this.socket.onopen = () => {
			console.log("WebSocket 连接已建立");
			this.reconnectAttempts = 0;
			this.notifyStatus("connected");
		};
		this.socket.onmessage = (event) => {
			const data = JSON.parse(event.data);
			this.onMessage(data);
		};
		this.socket.onclose = (event) => {
			console.log("WebSocket 连接已关闭", event.code, event.reason);
			this.notifyStatus("disconnected");

			// 非手动关闭时尝试重连
			if (!this.isManualClose) {
				this.scheduleReconnect();
			}
		};
		this.socket.onerror = (error) => {
			console.error("WebSocket 错误:", error);
		};
	}

	/** 发送消息 */
	send(data: Record<string, unknown>) {
		if (this.socket && this.socket.readyState === WebSocket.OPEN) {
			this.socket.send(JSON.stringify(data));
		}
	}

	/** 关闭连接 */
	close() {
		this.isManualClose = true;
		this.clearReconnectTimer();
		if (this.socket) {
			this.socket.close();
			this.socket = null;
		}
		this.notifyStatus("disconnected");
	}

	/** 安排重连 */
	private scheduleReconnect() {
		if (this.reconnectAttempts >= this.reconnectConfig.maxRetries) {
			console.error(
				`WebSocket 重连失败，已达到最大重试次数 ${this.reconnectConfig.maxRetries}`,
			);
			return;
		}

		this.notifyStatus("reconnecting");

		// 指数退避策略
		const delay = Math.min(
			this.reconnectConfig.initialDelay * 2 ** this.reconnectAttempts,
			this.reconnectConfig.maxDelay,
		);

		console.log(
			`WebSocket 将在 ${delay}ms 后重连 (第 ${this.reconnectAttempts + 1} 次)`,
		);

		this.reconnectTimer = setTimeout(() => {
			this.reconnectAttempts++;
			this.connect();
		}, delay);
	}

	/** 清除重连定时器 */
	private clearReconnectTimer() {
		if (this.reconnectTimer) {
			clearTimeout(this.reconnectTimer);
			this.reconnectTimer = null;
		}
	}

	/** 通知连接状态变化 */
	private notifyStatus(
		status: "connecting" | "connected" | "disconnected" | "reconnecting",
	) {
		this.onStatus?.(status);
	}
}
