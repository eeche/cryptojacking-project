from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import pandas as pd

# 데이터 로드
data_path = './Data/features_based_time.csv'
data = pd.read_csv(data_path)

# 특성과 레이블 분리
X = data.iloc[:, :-1]
y = data.iloc[:, -1]

# 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# 하이퍼파라미터 그리드 정의
param_grid = {
    'n_estimators': [100, 200, 300],
    'learning_rate': [0.01, 0.05, 0.1],
    'max_depth': [3, 4, 5],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'subsample': [0.8, 0.9, 1.0]
}

# 모델 생성
gbm_model = GradientBoostingClassifier(random_state=42)

# GridSearchCV 객체 생성
grid_search = GridSearchCV(estimator=gbm_model, param_grid=param_grid,
                           cv=3, n_jobs=-1, verbose=2)
# 결과
# Best parameters found: {'learning_rate': 0.1, 'max_depth': 5, 'min_samples_leaf': 4, 'min_samples_split': 10, 'n_estimators': 300, 'subsample': 0.8}
# Best cross-validation score: 0.9125129882029138

# 그리드 서치 수행
grid_search.fit(X_train, y_train)

# 최적의 하이퍼파라미터 출력
print(f"Best parameters found: {grid_search.best_params_}")
print(f"Best cross-validation score: {grid_search.best_score_}")

# 최적의 모델로 예측 수행
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)

print(f"정확도: {accuracy_score(y_test, y_pred) * 100: .2f}%")
print("분류 보고서:\n", classification_report(y_test, y_pred))

# 최적의 모델 저장
joblib.dump(best_model, 'best_gbm_model.pkl')

# 모델 불러오기
model_loaded = joblib.load('best_gbm_model.pkl')

# 불러온 모델로 예측 수행
y_pred_loaded = model_loaded.predict(X_test)

print(f"불러온 모델의 정확도: {accuracy_score(y_test, y_pred_loaded) * 100: .2f}%")
print("불러온 모델의 분류 보고서:\n", classification_report(y_test, y_pred_loaded))
