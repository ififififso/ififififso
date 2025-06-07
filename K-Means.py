import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 加载电力负荷数据 (假设CSV格式，包含日期时间和负荷值)
data = pd.read_excel('风光数据.xlsx', parse_dates=['时间'], index_col='时间')

# 示例数据格式:
# datetime,load,temperature,humidity,is_holiday
# 2023-01-01 00:00:00, 1250.5, 15.2, 65, 1
# 2023-01-01 01:00:00, 1180.3, 14.8, 67, 1
# ...

# 可视化原始数据
plt.figure(figsize=(15, 5))
data['load'].plot(title='Historical Load Data')
plt.ylabel('Load (MW)')
plt.xlabel('Date')
plt.show()

# 处理缺失值
data.fillna(method='ffill', inplace=True)  # 前向填充

# 添加时间特征
data['hour'] = data.index.hour
data['day_of_week'] = data.index.dayofweek
data['month'] = data.index.month
data['is_weekend'] = data['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)

# 标准化/归一化
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
data['load_scaled'] = scaler.fit_transform(data[['load']])

# 检查数据
print(data.head())

# 添加滞后特征 (过去24小时的负荷)
#for i in range(1, 25):
#data[f'load_lag_{i}'] = data['load_scaled'].shift(i)

# 添加移动平均特征
data['load_ma_24'] = data['load_scaled'].rolling(window=24).mean()

# 添加温度相关特征 (如果数据中有温度)
if 'temperature' in data.columns:
    data['temp_lag_24'] = data['temperature'].shift(24)
    data['temp_diff'] = data['temperature'] - data['temp_lag_24']

# 删除包含NaN的行 (由于滞后特征引入的)
#data.dropna(inplace=True)

# 分离特征和目标
X = data.drop(['load', 'load_scaled'], axis=1, errors='ignore')
y = data['load_scaled']

# 划分训练集和测试集
split_date = '2023-10-01'  # 根据实际数据调整
X_train = X[X.index < split_date]
X_test = X[X.index >= split_date]
y_train = y[y.index < split_date]
y_test = y[y.index >= split_date]

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

# 训练模型
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# 预测
y_pred_rf = rf.predict(X_test)

# 反归一化
y_test_actual = scaler.inverse_transform(y_test.values.reshape(-1, 1))
y_pred_rf_actual = scaler.inverse_transform(y_pred_rf.reshape(-1, 1))

# 评估
mae_rf = mean_absolute_error(y_test_actual, y_pred_rf_actual)
rmse_rf = np.sqrt(mean_squared_error(y_test_actual, y_pred_rf_actual))
print(f"Random Forest - MAE: {mae_rf:.2f}, RMSE: {rmse_rf:.2f}")

# 可视化预测结果
plt.figure(figsize=(15, 5))
plt.plot(y_test.index, y_test_actual, label='Actual')
plt.plot(y_test.index, y_pred_rf_actual, label='Predicted', alpha=0.7)
plt.title('Random Forest Load Forecasting')
plt.ylabel('Load (MW)')
plt.legend()
plt.show()

