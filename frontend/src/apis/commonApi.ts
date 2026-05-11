import request from "@/utils/request";
import type { Message } from "@/utils/response";

/** 健康检查 */
export function getHelloWorld() {
	return request.get<{ message: string }>("/");
}

/** 获取论文写作顺序 */
export function getWriterSeque() {
	return request.get<{ writer_seque: string[] }>("/writer_seque");
}

/**
 * 获取任务的历史消息
 * @param task_id 任务ID
 */
export function getTaskMessages(task_id: string) {
	return request.get<Message[]>("/messages", {
		params: {
			task_id,
		},
	});
}

/**
 * 打开工作目录
 * @param task_id 任务ID
 */
export function openFolderAPI(task_id: string) {
	return request.get<{ message: string }>("/open_folder", {
		params: {
			task_id,
		},
	});
}

/**
 * 提交样例任务
 * @param example_id 样例ID
 * @param source 来源
 */
export function exampleAPI(example_id: string, source: string) {
	return request.post<{
		task_id: string;
		status: string;
	}>("/example", {
		example_id,
		source,
	});
}

/** 获取后端和 Redis 服务状态 */
export function getServiceStatus() {
	return request.get<{
		backend: { status: string; message: string };
		redis: { status: string; message: string };
	}>("/status");
}
