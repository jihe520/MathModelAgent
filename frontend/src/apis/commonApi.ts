import request from "@/utils/request";

export function getHelloWorld() {
	return request.get<{ message: string }>("/");
}

// 获取论文顺序
export function getWriterSeque() {
	return request.get<{ writer_seque: string[] }>("/writer_seque");
}


export function openFolderAPI(task_id: string) {
	return request.get<{ message: string }>("/open_folder", {
		params: {
			task_id,
		},
	});
}


export function exampleAPI(example_id: string, source: string) {
	return request.post<{
		task_id: string;
		status: string;
	}>("/example", {
		example_id,
		source,
	});
}

// 获取服务状态
export function getServiceStatus() {
	return request.get<{
		backend: { status: string; message: string };
		redis: { status: string; message: string };
	}>("/status");
}