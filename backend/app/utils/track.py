"""LLM 调用指标收集模块。"""

from litellm.integrations.custom_logger import CustomLogger  # type: ignore[import-unresolved]


class AgentMetrics(CustomLogger):
    """LLM 调用指标收集器，记录成功的 API 调用信息。"""

    async def async_log_success_event(self, kwargs, response_obj, start_time, end_time):
        try:
            # response_cost = kwargs.get("response_cost", 0)
            # print("streaming response_cost", response_cost)
            print("agent_name", kwargs["litellm_params"]["metadata"]["agent_name"])
        except Exception:
            pass

    async def async_log_failure_event(self, kwargs, response_obj, start_time, end_time):
        print("On Async Failure")


# 全局指标收集器实例
agent_metrics = AgentMetrics()
