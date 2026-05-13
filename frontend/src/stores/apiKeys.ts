import { AgentType } from "@/utils/enum";
import type { ModelConfig } from "@/utils/interface";
import { defineStore } from "pinia";
import { computed, ref } from "vue";

/** API Key 和模型配置 Store */
export const useApiKeyStore = defineStore(
	"apiKeys",
	() => {
		// ---- State ----

		/** 协调者模型配置 */
		const coordinatorConfig = ref<ModelConfig>({
			apiKey: "",
			baseUrl: "",
			modelId: "",
			apiType: "",
			contextWindow: 128000,
		});

		/** 建模者模型配置 */
		const modelerConfig = ref<ModelConfig>({
			apiKey: "",
			baseUrl: "",
			modelId: "",
			apiType: "",
			contextWindow: 128000,
		});

		/** 编码者模型配置 */
		const coderConfig = ref<ModelConfig>({
			apiKey: "",
			baseUrl: "",
			modelId: "",
			apiType: "",
			contextWindow: 128000,
		});

		/** 写作者模型配置 */
		const writerConfig = ref<ModelConfig>({
			apiKey: "",
			baseUrl: "",
			modelId: "",
			apiType: "",
			contextWindow: 128000,
		});

		/** OpenAlex 邮箱 */
		const openalexEmail = ref<string>("");

		// ---- Getters ----

		/** 判断所有配置是否为空 */
		const isEmpty = computed(() => {
			return Object.values(getAllAgentConfigs()).every(
				(config) => config.apiKey === "",
			);
		});

		// ---- Actions ----

		/** 设置协调者模型配置 */
		function setCoordinatorConfig(config: ModelConfig) {
			coordinatorConfig.value = { ...config };
		}

		/** 设置建模者模型配置 */
		function setModelerConfig(config: ModelConfig) {
			modelerConfig.value = { ...config };
		}

		/** 设置编码者模型配置 */
		function setCoderConfig(config: ModelConfig) {
			coderConfig.value = { ...config };
		}

		/** 设置写作者模型配置 */
		function setWriterConfig(config: ModelConfig) {
			writerConfig.value = { ...config };
		}

		/** 设置 OpenAlex 邮箱 */
		function setOpenalexEmail(email: string) {
			console.log("setOpenalexEmail", email);
			openalexEmail.value = email;
		}

		/** 获取所有 Agent 的模型配置 */
		function getAllAgentConfigs() {
			return {
				[AgentType.COORDINATOR]: coordinatorConfig.value,
				[AgentType.MODELER]: modelerConfig.value,
				[AgentType.CODER]: coderConfig.value,
				[AgentType.WRITER]: writerConfig.value,
			};
		}

		/** 重置所有配置为默认值 */
		function resetAll() {
			coordinatorConfig.value = {
				apiKey: "",
				baseUrl: "",
				modelId: "",
				apiType: "",
				contextWindow: 128000,
			};
			modelerConfig.value = {
				apiKey: "",
				baseUrl: "",
				modelId: "",
				apiType: "",
				contextWindow: 128000,
			};
			coderConfig.value = {
				apiKey: "",
				baseUrl: "",
				modelId: "",
				apiType: "",
				contextWindow: 128000,
			};
			writerConfig.value = {
				apiKey: "",
				baseUrl: "",
				modelId: "",
				apiType: "",
				contextWindow: 128000,
			};
			openalexEmail.value = "";
		}

		return {
			// 状态
			coordinatorConfig,
			modelerConfig,
			coderConfig,
			writerConfig,
			openalexEmail,
			isEmpty,

			// 方法
			setCoordinatorConfig,
			setModelerConfig,
			setCoderConfig,
			setWriterConfig,
			setOpenalexEmail,
			getAllAgentConfigs,
			resetAll,
		};
	},
	{
		persist: true, // 启用持久化存储
	},
);
