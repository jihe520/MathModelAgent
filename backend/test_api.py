import asyncio  
import litellm  
  
async def validate_model_api(api_key: str, base_url: str, model_id: str):  
    """  
    验证模型 API 是否可用的最小脚本  
      
    Args:  
        api_key: API 密钥  
        base_url: API 基础 URL (例如: https://api.openai.com/v1)  
        model_id: 模型标识符 (例如: gpt-4, deepseek/deepseek-chat)  
      
    Returns:  
        dict: {"valid": bool, "message": str}  
    """  
    try:  
        # 构建请求参数  
        kwargs = {  
            "model": model_id,  
            "messages": [{"role": "user", "content": "Hi"}],  
            "max_tokens": 1,  
            "api_key": api_key,  
        }  
          
        # 只有当 base_url 存在时才添加  
        if base_url:  
            kwargs["base_url"] = base_url  
          
        # 发送测试请求  
        await litellm.acompletion(**kwargs)  
          
        return {  
            "valid": True,  
            "message": "✓ 模型 API 验证成功"  
        }  
          
    except Exception as e:  
        error_msg = str(e)  
          
        # 解析常见错误类型  
        if "401" in error_msg or "Unauthorized" in error_msg:  
            message = "✗ API Key 无效或已过期"  
        elif "404" in error_msg or "Not Found" in error_msg:  
            message = "✗ 模型 ID 不存在或 Base URL 错误"  
        elif "429" in error_msg or "rate limit" in error_msg.lower():  
            message = "✗ 请求过于频繁,请稍后再试"  
        elif "403" in error_msg or "Forbidden" in error_msg:  
            message = "✗ API 权限不足或账户余额不足"  
        else:  
            message = f"✗ 验证失败: {error_msg[:100]}"  
          
        return {  
            "valid": False,  
            "message": message  
        }  
  
  
# 使用示例  
async def main():  

    result = await validate_model_api(  
        api_key="",  
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        model_id="openai/qwen3-max"
    )  
    print(f"Qwen: {result}")  
      
  
if __name__ == "__main__":  
    asyncio.run(main())
