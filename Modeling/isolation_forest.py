import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import pandas as pd
from sklearn.ensemble import IsolationForest

data_path = './Data/features_based_time.csv'
data = pd.read_csv(data_path)

X = data.iloc[:, :-1]
y = data.iloc[:, -1]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# Isolation Forest 모델 생성 및 학습
isolation_forest_model = IsolationForest(n_estimators=100, random_state=42)
isolation_forest_model.fit(X_train)

# 모델 저장 및 불러오기
joblib.dump(isolation_forest_model, 'isolation_forest_model.pkl')
model_loaded = joblib.load('isolation_forest_model.pkl')

# 모델 예측 함수 (Isolation Forest는 이상치를 감지하기 때문에, 반환 값이 -1이면 이상치, 1이면 정상)
y_pred = model_loaded.predict(X_test)
y_pred = [1 if x == 1 else 0 for x in y_pred]  # 정상을 1, 이상치를 0으로 변환

print(f"정확도: {accuracy_score(y_test, y_pred) * 100: .2f}%")
print("분류 보고서:\n", classification_report(y_test, y_pred))
