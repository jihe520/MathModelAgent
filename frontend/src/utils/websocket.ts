/** WebSocket 消息处理回调函数类型 */
type MessageHandler = (data: unknown) => void;

/** 任务 WebSocket 连接管理类 */
export class TaskWebSocket {
	private socket: WebSocket | null = null;
	private url: string;
	private onMessage: MessageHandler;

	constructor(url: string, onMessage: MessageHandler) {
		this.url = url;
		this.onMessage = onMessage;
	}

	/** 建立 WebSocket 连接 */
	connect() {
		this.socket = new WebSocket(this.url);
		this.socket.onopen = () => {
			console.log("WebSocket 连接已建立");
		};
		this.socket.onmessage = (event) => {
			const data = JSON.parse(event.data);
			this.onMessage(data);
		};
		this.socket.onclose = (event) => {
			console.log("WebSocket 连接已关闭", event.code, event.reason);
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
		if (this.socket) {
			this.socket.close();
		}
	}
}
