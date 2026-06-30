# Figure Template Catalog

Each id maps to a bundled script under `scripts/templates/`.

| id | script | figure |
| --- | --- | --- |
| `multiclass-shap-combo` | `make_multiclass_shap_combo.py` | 多分类 SHAP 柱状图与蜂群图组合图 |
| `paired-raincloud` | `make_paired_raincloud.py` | 配对云雨图 |
| `cv-roc-ci` | `make_cv_roc_ci.py` | 交叉验证 ROC 曲线与置信区间图 |
| `taylor-diagram` | `make_taylor_diagram.py` | 多模型评价泰勒图 |
| `correlation-pairgrid` | `make_correlation_pairgrid.py` | 数据分布、拟合线、置信区间、相关系数组合图 |
| `prediction-marginal-grid` | `make_prediction_marginal_grid.py` | 预测值与真实值边缘分布组合图 |
| `rf-tpe-surface` | `make_rf_tpe_surface.py` | TPE 优化 RF 模型 3D 曲面图 |
| `grouped-corr-split-violin` | `make_grouped_corr_split_violin.py` | 下三角相关矩阵 + 特征分组与半边小提琴图 |
| `grouped-circular-heatmap` | `make_grouped_circular_heatmap.py` | 分组环形热图 |
| `urban-park-cooling-combo` | `make_urban_park_cooling_combo.py` | 堆叠图 + 云雨图 + 箱线图组合图 |
| `nature-chord-diagram` | `make_nature_chord_diagram.py` | Nature 风格和弦图 |

Prompts from the MathModel Improve tab should include `$mathmodel-figure-templates` and the human-readable figure title. The agent should convert that title to one of the ids above and call `scripts/render_template.py`.
