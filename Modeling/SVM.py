import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC  # SVM 분류기를 위해 SVC 클래스를 임포트합니다.
from sklearn.metrics import classification_report, accuracy_score
import pandas as pd

# 데이터 경로 지정
data_path = './Data/features_based_time.csv'
data = pd.read_csv(data_path)

# 데이터셋에서 피처(X)와 타겟(y) 분리
X = data.iloc[:, :-1]
y = data.iloc[:, -1]

# 데이터셋을 훈련 세트와 테스트 세트로 분할
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# 데이터 스케일링
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
print("Scaled X_train shape:", X_train.shape)
print("Scaled X_test shape:", X_test.shape)
print("First 5 rows of scaled X_train:\n", X_train[:5])

# SVM 모델 생성 및 훈련
# SVM 모델을 생성합니다. 커널은 'linear'로 설정합니다.
svm_model = SVC(kernel='linear', random_state=42)
svm_model.fit(X_train, y_train)

# 모델 저장 및 불러오기
joblib.dump(svm_model, 'svm_model.pkl')  # SVM 모델을 파일로 저장합니다.
joblib.dump(scaler, 'scaler.pkl')  # 스케일러를 파일로 저장합니다.
model_loaded = joblib.load('svm_model.pkl')  # 저장된 SVM 모델을 불러옵니다.

# 모델을 사용한 예측
y_pred = model_loaded.predict(X_test)

# 모델 성능 평가
print(f"정확도:, {accuracy_score(y_test, y_pred) * 100: .2f}%")
print("분류 보고서:\n", classification_report(y_test, y_pred))
