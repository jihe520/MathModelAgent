import request from "@/utils/request";

/** 验证 API Key 请求参数 */
export interface ValidateApiKeyRequest {
	api_key: string;
	base_url?: string;
	model_id: string;
}

/** 验证 API Key 响应 */
export interface ValidateApiKeyResponse {
	valid: boolean;
	message: string;
}

/** 保存 API 配置请求参数 */
export interface SaveApiConfigRequest {
	coordinator: {
		apiKey: string;
		baseUrl: string;
		modelId: string;
		provider: string;
	};
	modeler: {
		apiKey: string;
		baseUrl: string;
		modelId: string;
		provider: string;
	};
	coder: {
		apiKey: string;
		baseUrl: string;
		modelId: string;
		provider: string;
	};
	writer: {
		apiKey: string;
		baseUrl: string;
		modelId: string;
		provider: string;
	};
	openalex_email: string;
}

/** 验证 OpenAlex Email 请求参数 */
export interface ValidateOpenalexEmailRequest {
	email: string;
}

/** 验证 OpenAlex Email 响应 */
export interface ValidateOpenalexEmailResponse {
	valid: boolean;
	message: string;
}

/**
 * 验证 API Key 是否有效
 * @param params 验证请求参数
 */
export function validateApiKey(params: ValidateApiKeyRequest) {
	return request.post<ValidateApiKeyResponse>("/validate-api-key", params);
}

/**
 * 验证 OpenAlex Email 是否有效
 * @param params 验证请求参数
 */
export function validateOpenalexEmail(params: ValidateOpenalexEmailRequest) {
	return request.post<ValidateOpenalexEmailResponse>(
		"/validate-openalex-email",
		params,
	);
}

/**
 * 保存 API 配置到后端
 * @param params API 配置参数
 */
export function saveApiConfig(params: SaveApiConfigRequest) {
	return request.post<{ success: boolean; message: string }>(
		"/save-api-config",
		params,
	);
}
