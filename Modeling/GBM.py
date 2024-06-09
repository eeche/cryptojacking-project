from sklearn.ensemble import GradientBoostingClassifier
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import pandas as pd

data_path = 'C:\\Users\\dlckd\\Desktop\\cryptoProject\\Data\\features_based_time.csv'
data = pd.read_csv(data_path)

X = data.iloc[:, :-1]
y = data.iloc[:, -1]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)
# GBM 모델 생성 및 학습
gbm_model = GradientBoostingClassifier(n_estimators=100, random_state=42)
gbm_model.fit(X_train, y_train)

# 모델 저장 및 불러오기
joblib.dump(gbm_model, 'gbm_model.pkl')
model_loaded = joblib.load('gbm_model.pkl')

# 모델 예측 함수
y_pred = model_loaded.predict(X_test)

print(f"정확도: {accuracy_score(y_test, y_pred) * 100: .2f}%")
print("분류 보고서:\n", classification_report(y_test, y_pred))
