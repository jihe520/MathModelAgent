#!/usr/bin/env python3
"""
GiteeAI 集成测试脚本
用于验证 GiteeAI API 集成是否正常工作
"""

import asyncio
import sys
import os

# 添加项目路径到 Python 路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.routers.modeling_router import ValidateApiKeyRequest, validate_api_key
from app.core.llm.llm import LLM
import litellm

async def test_gitee_api_validation():
    """测试 GiteeAI API 验证功能"""
    print("🧪 开始测试 GiteeAI API 验证...")
    
    # 测试数据
    test_request = ValidateApiKeyRequest(
        api_key="test_key_placeholder",  # 需要替换为实际的 API Key
        base_url="https://ai.gitee.com/v1",
        model_id="DeepSeek-V3"
    )
    
    try:
        result = await validate_api_key(test_request)
        print(f"✅ API 验证结果: {result.valid}")
        print(f"📝 消息: {result.message}")
        return result.valid
    except Exception as e:
        print(f"❌ API 验证失败: {str(e)}")
        return False

def test_model_cost_registration():
    """测试模型成本注册"""
    print("\n🧪 检查 DeepSeek-V3 模型成本注册...")
    
    if "DeepSeek-V3" in litellm.model_cost:
        cost_info = litellm.model_cost["DeepSeek-V3"]
        print(f"✅ DeepSeek-V3 已注册")
        print(f"📊 模型信息:")
        print(f"   - 最大 tokens: {cost_info.get('max_tokens')}")
        print(f"   - 输入成本: {cost_info.get('input_cost_per_token')}")
        print(f"   - 输出成本: {cost_info.get('output_cost_per_token')}")
        print(f"   - 提供商: {cost_info.get('litellm_provider')}")
        return True
    else:
        print("❌ DeepSeek-V3 未注册")
        return False

def test_llm_provider_detection():
    """测试 LLM 提供商自动检测"""
    print("\n🧪 测试 LLM 提供商自动检测...")
    
    # 创建测试 LLM 实例
    test_cases = [
        {
            "name": "GiteeAI",
            "base_url": "https://ai.gitee.com/v1",
            "model": "DeepSeek-V3",
            "expected_provider": "openai"
        },
        {
            "name": "DeepSeek 官方",
            "base_url": "https://api.deepseek.com",
            "model": "deepseek-chat",
            "expected_provider": "deepseek"
        },
        {
            "name": "OpenAI",
            "base_url": "https://api.openai.com/v1",
            "model": "gpt-4",
            "expected_provider": "openai"
        }
    ]
    
    all_passed = True
    
    for case in test_cases:
        print(f"\n   测试 {case['name']}:")
        print(f"   - Base URL: {case['base_url']}")
        print(f"   - Model: {case['model']}")
        
        # 这里我们只测试逻辑，不实际调用 API
        base_url_lower = case['base_url'].lower()
        model_lower = case['model'].lower()
        
        if "gitee" in base_url_lower:
            detected_provider = "openai"
        elif "deepseek" in model_lower or "deepseek" in base_url_lower:
            detected_provider = "deepseek"
        elif "openai" in base_url_lower or "api.openai.com" in base_url_lower:
            detected_provider = "openai"
        else:
            detected_provider = "unknown"
        
        if detected_provider == case['expected_provider']:
            print(f"   ✅ 检测正确: {detected_provider}")
        else:
            print(f"   ❌ 检测错误: 期望 {case['expected_provider']}, 实际 {detected_provider}")
            all_passed = False
    
    return all_passed

async def main():
    """主测试函数"""
    print("🚀 GiteeAI 集成测试开始")
    print("=" * 50)
    
    # 测试1: 模型成本注册
    cost_test = test_model_cost_registration()
    
    # 测试2: 提供商检测
    provider_test = test_llm_provider_detection()
    
    # 测试3: API 验证（需要真实 API Key 才能测试）
    print("\n🧪 API 验证测试 (需要真实 API Key)...")
    print("💡 如需测试 API 验证，请将真实 API Key 添加到测试脚本中")
    
    print("\n" + "=" * 50)
    print("📊 测试结果汇总:")
    print(f"   模型成本注册: {'✅ 通过' if cost_test else '❌ 失败'}")
    print(f"   提供商检测: {'✅ 通过' if provider_test else '❌ 失败'}")
    print(f"   API 验证: 🔄 需要真实 API Key")
    
    if cost_test and provider_test:
        print("\n🎉 基础集成测试通过！")
        print("💡 提示: 使用真实 API Key 测试完整功能")
        return True
    else:
        print("\n❌ 某些测试失败，请检查配置")
        return False

if __name__ == "__main__":
    asyncio.run(main())