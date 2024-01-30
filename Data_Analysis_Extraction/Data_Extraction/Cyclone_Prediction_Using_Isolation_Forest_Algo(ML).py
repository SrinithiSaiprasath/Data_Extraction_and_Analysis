import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


df = pd.read_csv('GPP_12.5_86.0.csv')  # Replace with your actual file path
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)
df['GPP_Rate'] = df['GPP'].diff()

plt.figure(figsize=(12, 6))
sns.lineplot(x=df.index, y='GPP', data=df, label='GPP')
sns.lineplot(x=df.index, y='GPP', data=df, label='GPP Rate of Change')
plt.title('GPP and Rate of Change Over Time')
plt.xlabel('Date')
plt.ylabel('GPP')
plt.legend()
plt.show()

X = df[['GPP']].values
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = IsolationForest(contamination=0.05, random_state=42)
df['Anomaly'] = model.fit_predict(X_scaled)

plt.figure(figsize=(12, 6))
sns.lineplot(x=df.index, y='GPP', data=df, label='GPP')
plt.scatter(df[df['Anomaly'] == -1].index, df[df['Anomaly'] == -1]['GPP'], color='red', label='Anomalies')
plt.title('GPP with Anomalies Detected')
plt.xlabel('Date')
plt.ylabel('GPP')
plt.legend()
plt.show()

anomalies = df[df['Anomaly'] == -1].index
print("Dates with Anomalies:")
with open('MLxAnomalies.txt' , 'w') as f:
    for anomalie in anomalies:
        f.write(f'{anomalie.date()} \n')
print('done')

