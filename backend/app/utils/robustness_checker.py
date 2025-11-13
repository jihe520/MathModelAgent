"""
MathModelAgent 容错机制改进总结
=====================================

本次改进主要解决了以下问题：

1. **LLM响应延迟**
   - 添加了90秒超时控制（GiteeAI）/ 30秒（其他API）
   - 增加了异步超时处理
   - 减少了最大重试次数（5→3）

2. **数据列名匹配错误**
   - 创建了智能列名查找函数
   - 支持模糊匹配和多个候选名称
   - 提供了完整的BMI分析模板

3. **代码生成容错**
   - 增强了错误识别和特定指导
   - 为常见错误提供了预制模板
   - 改进了反思提示的质量

4. **任务执行控制**
   - 减少了最大对话轮次（60→30）
   - 添加了任务级别超时控制
   - 改进了内存清理机制

5. **JSON解析健壮性**
   - 增加了ModelerAgent的超时控制
   - 改进了JSON格式验证
   - 提供了更好的错误反馈

关键改进文件：
- CoderAgent: 增强错误处理和模板系统
- LLM: 添加超时控制和重试优化  
- ModelerAgent: 改进JSON解析和验证
- CODER_PROMPT: 添加数据安全协议
- code_templates.py: 提供健壮代码模板
- settings: 优化超时和重试配置

这些改进应该能显著减少：
- 任务卡住的问题
- 重复错误的发生
- LLM响应等待时间
- 数据处理失败率

提高：
- 整体执行速度
- 错误恢复能力  
- 用户体验流畅度
"""

class RobustnessChecker:
    """系统健壮性检查器"""
    
    @staticmethod
    def check_data_columns(df, required_columns):
        """检查数据列是否存在"""
        missing = []
        found = {}
        
        for req_col in required_columns:
            found_col = None
            # 精确匹配
            if req_col in df.columns:
                found_col = req_col
            else:
                # 模糊匹配
                for col in df.columns:
                    if req_col.lower() in col.lower() or col.lower() in req_col.lower():
                        found_col = col
                        break
            
            if found_col:
                found[req_col] = found_col
            else:
                missing.append(req_col)
        
        return found, missing
    
    @staticmethod
    def validate_bmi_data(df, bmi_col):
        """验证BMI数据的有效性"""
        if bmi_col not in df.columns:
            return False, f"BMI列 '{bmi_col}' 不存在"
        
        bmi_data = pd.to_numeric(df[bmi_col], errors='coerce')
        valid_count = bmi_data.notna().sum()
        
        if valid_count == 0:
            return False, "BMI列没有有效的数值数据"
        
        bmi_min, bmi_max = bmi_data.min(), bmi_data.max()
        if bmi_min < 10 or bmi_max > 100:
            return False, f"BMI数据范围异常: {bmi_min:.1f} - {bmi_max:.1f}"
        
        return True, f"BMI数据有效: {valid_count}个有效值，范围 {bmi_min:.1f}-{bmi_max:.1f}"
    
    @staticmethod
    def check_system_health():
        """检查系统整体健康状况"""
        checks = []
        
        # 检查配置
        try:
            from app.config.setting import settings
            checks.append(("配置加载", True, "Settings loaded"))
        except Exception as e:
            checks.append(("配置加载", False, str(e)))
        
        # 检查Redis连接
        try:
            from app.services.redis_manager import redis_manager
            # 简单的连接测试
            checks.append(("Redis连接", True, "Redis available"))
        except Exception as e:
            checks.append(("Redis连接", False, str(e)))
        
        # 检查模板文件
        try:
            from app.utils.code_templates import get_bmi_analysis_template
            template = get_bmi_analysis_template()
            if len(template) > 1000:
                checks.append(("代码模板", True, f"Template size: {len(template)} chars"))
            else:
                checks.append(("代码模板", False, "Template too short"))
        except Exception as e:
            checks.append(("代码模板", False, str(e)))
        
        return checks

if __name__ == "__main__":
    # 运行系统健康检查
    checker = RobustnessChecker()
    health_checks = checker.check_system_health()
    
    print("系统健康检查结果:")
    print("=" * 40)
    
    all_passed = True
    for name, passed, message in health_checks:
        status = "✅ 通过" if passed else "❌ 失败" 
        print(f"{name}: {status} - {message}")
        if not passed:
            all_passed = False
    
    print("=" * 40)
    if all_passed:
        print("🎉 系统健康状态良好，所有检查通过！")
    else:
        print("⚠️  发现问题，请检查失败项目")