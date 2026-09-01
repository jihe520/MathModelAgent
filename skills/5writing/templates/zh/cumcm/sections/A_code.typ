#heading(level: 2, numbering: none)[支撑材料文件列表]

电子支撑材料与参赛论文分开提交；此处按最终支撑材料逐项列出文件名及用途。

#heading(level: 2, numbering: none)[完整源程序]

#v(1.1em)

```python
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

data = pd.read_csv('data.csv')
X = data.drop('target', axis=1); y = data['target']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
print(f'R2: {r2_score(y_test, model.predict(X_test)):.4f}')
```
