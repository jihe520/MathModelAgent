"""
代码模板工具 - 提供健壮的数据分析代码模板
"""

def get_bmi_analysis_template():
    """获取BMI分组分析的健壮代码模板"""
    return '''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import sem

# 设置中文显示
plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

print("=== 开始BMI分组分析 ===")

# 1. 数据加载（多重备选方案）
df = None
for filename in ["清洗后的数据.xlsx", "附件.xlsx"]:
    try:
        df = pd.read_excel(filename)
        print(f"✓ 成功加载数据: {filename}")
        break
    except Exception as e:
        print(f"✗ 加载 {filename} 失败: {e}")
        continue

if df is None:
    raise FileNotFoundError("未找到可用的数据文件")

# 2. 列名智能映射
def smart_find_column(df, keywords, description=""):
    """智能查找列名"""
    cols = df.columns.tolist()
    print(f"查找{description}，候选关键词: {keywords}")
    
    for keyword in keywords:
        # 精确匹配
        if keyword in cols:
            print(f"  ✓ 精确匹配: {keyword}")
            return keyword
        # 包含匹配
        for col in cols:
            if keyword in str(col):
                print(f"  ✓ 部分匹配: {col} (含{keyword})")
                return col
    
    print(f"  ✗ 未找到{description}")
    return None

# 查找关键列
week_col = smart_find_column(df, ['检测孕周', '孕周', 'week'], "孕周列")
bmi_col = smart_find_column(df, ['孕妇BMI', 'BMI'], "BMI列")
y_col = smart_find_column(df, ['Y染色体浓度', 'Y浓度', 'Y'], "Y染色体浓度列")
id_col = smart_find_column(df, ['孕妇代码', '受试者ID', '序号'], "标识列")

# 验证必需列
required_cols = {'孕周': week_col, 'BMI': bmi_col, 'Y染色体浓度': y_col}
missing_cols = [k for k, v in required_cols.items() if v is None]

if missing_cols:
    print(f"❌ 缺少必需列: {missing_cols}")
    print(f"可用列: {df.columns.tolist()}")
    raise KeyError(f"数据中缺少必需的列: {missing_cols}")

print("✓ 所有必需列已找到")

# 3. 数据预处理
print("\\n=== 数据预处理 ===")
for desc, col in required_cols.items():
    if col:
        df[desc] = pd.to_numeric(df[col], errors="coerce")
        valid_count = df[desc].notna().sum()
        print(f"{desc}: {valid_count} 个有效值")

# 4. BMI分组（动态调整范围）
bmi_values = df['BMI'].dropna()
if len(bmi_values) == 0:
    raise ValueError("没有有效的BMI数据")

bmi_min, bmi_max = bmi_values.min(), bmi_values.max()
print(f"BMI范围: {bmi_min:.1f} - {bmi_max:.1f}")

# 使用合理的分组区间
if bmi_max <= 35:
    bins = [0, 25, 30, 35, np.inf]
    labels = ["<25", "[25,30)", "[30,35)", "≥35"]
else:
    bins = [0, 28, 32, 36, 40, np.inf]
    labels = ["<28", "[28,32)", "[32,36)", "[36,40)", "≥40"]

df["BMI组"] = pd.cut(df["BMI"], bins=bins, labels=labels, right=False)

# 检查分组结果
group_counts = df["BMI组"].value_counts().sort_index()
print(f"\\n各组样本数:")
for group, count in group_counts.items():
    print(f"  {group}: {count}个")

# 5. 计算最早达标时间（简化版本，避免复杂的受试者分组）
print("\\n=== 计算各组统计 ===")
results = []

for group in labels:
    group_data = df[df["BMI组"] == group]
    
    if len(group_data) == 0:
        print(f"{group}: 无数据")
        results.append({"BMI组": group, "均值": np.nan, "标准误": np.nan, "样本数": 0})
        continue
    
    # 过滤有效数据
    valid_data = group_data.dropna(subset=['孕周', 'Y染色体浓度'])
    
    if len(valid_data) == 0:
        print(f"{group}: 无有效数据")
        results.append({"BMI组": group, "均值": np.nan, "标准误": np.nan, "样本数": 0})
        continue
    
    # 计算孕周统计（不依赖Y染色体浓度阈值，避免过滤后数据为空）
    weeks = valid_data['孕周'].values
    mean_week = np.mean(weeks)
    std_err = sem(weeks) if len(weeks) > 1 else 0
    
    print(f"{group}: {len(weeks)}个样本, 平均孕周 {mean_week:.1f}±{std_err:.2f}")
    results.append({
        "BMI组": group, 
        "均值": mean_week, 
        "标准误": std_err,
        "样本数": len(weeks)
    })

# 6. 结果整理和可视化
results_df = pd.DataFrame(results)
valid_results = results_df[results_df["样本数"] > 0].copy()

print(f"\\n=== 分析结果 ===")
if len(valid_results) == 0:
    print("❌ 没有有效的分析结果")
else:
    print("✓ 各组统计结果:")
    print(valid_results.to_string(index=False))
    
    # 绘制图表
    if len(valid_results) >= 2:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # 误差条图
        ax1.errorbar(
            valid_results["BMI组"], 
            valid_results["均值"],
            yerr=valid_results["标准误"],
            fmt='o-', capsize=5, linewidth=2, markersize=8
        )
        ax1.set_title("不同BMI组的平均检测孕周", fontsize=14)
        ax1.set_xlabel("BMI组", fontsize=12)
        ax1.set_ylabel("平均孕周", fontsize=12)
        ax1.grid(True, alpha=0.3)
        ax1.tick_params(axis='x', rotation=45)
        
        # 样本数条形图
        ax2.bar(valid_results["BMI组"], valid_results["样本数"], 
                color='lightblue', alpha=0.7)
        ax2.set_title("各BMI组样本数量", fontsize=14)
        ax2.set_xlabel("BMI组", fontsize=12)
        ax2.set_ylabel("样本数", fontsize=12)
        ax2.tick_params(axis='x', rotation=45)
        
        # 在条形图上显示数值
        for i, v in enumerate(valid_results["样本数"]):
            ax2.text(i, v + 0.5, str(int(v)), ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig("bmi_analysis_results.png", dpi=300, bbox_inches='tight')
        print("\\n✓ 图表已保存为 'bmi_analysis_results.png'")
        plt.show()
    else:
        print("数据不足，无法生成对比图表")

print("\\n=== 分析完成 ===")
'''

def get_safe_data_loading_template():
    """获取安全的数据加载模板"""
    return '''
import pandas as pd
import os

def safe_load_data():
    """安全加载数据，支持多种文件格式和容错"""
    
    # 候选文件列表（按优先级排序）
    candidate_files = [
        "清洗后的数据.xlsx",
        "附件.xlsx", 
        "data.xlsx",
        "数据.xlsx"
    ]
    
    # 扫描当前目录下的所有Excel文件
    excel_files = [f for f in os.listdir('.') if f.endswith(('.xlsx', '.xls'))]
    candidate_files.extend(excel_files)
    
    # 去重并保持顺序
    seen = set()
    unique_candidates = []
    for f in candidate_files:
        if f not in seen:
            unique_candidates.append(f)
            seen.add(f)
    
    print(f"候选数据文件: {unique_candidates}")
    
    # 逐个尝试加载
    for filename in unique_candidates:
        if not os.path.exists(filename):
            continue
            
        try:
            df = pd.read_excel(filename)
            if df.empty:
                print(f"⚠️  {filename} 文件为空")
                continue
                
            print(f"✅ 成功加载: {filename}")
            print(f"   数据形状: {df.shape}")
            print(f"   列数: {len(df.columns)}")
            return df, filename
            
        except Exception as e:
            print(f"❌ 加载 {filename} 失败: {str(e)}")
            continue
    
    # 如果都失败了，抛出异常
    raise FileNotFoundError(f"无法加载任何数据文件。尝试的文件: {unique_candidates}")

# 使用示例
df, loaded_file = safe_load_data()
print(f"\\n使用数据文件: {loaded_file}")
print(f"数据列名: {df.columns.tolist()}")
'''