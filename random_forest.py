import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import pandas as pd

# data_path = 'new_frequency_features_corrected.csv'
data_path = 'C:\\Users\\dlckd\\Desktop\\cryptoProject\\Data\\features_based_time.csv'
data = pd.read_csv(data_path)

X = data.iloc[:, :-1]
y = data.iloc[:, -1]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
print("Scaled X_train shape:", X_train.shape)
print("Scaled X_test shape:", X_test.shape)
print("First 5 rows of scaled X_train:\n", X_train[:5])


random_forest_model = RandomForestClassifier(n_estimators=10, random_state=42)
random_forest_model.fit(X_train, y_train)
joblib.dump(random_forest_model, 'random_forest_model.pkl')
joblib.dump(scaler, 'scaler.pkl')
model_loaded = joblib.load('random_forest_model.pkl')
# 모델 예측 함수
y_pred = model_loaded.predict(X_test)

print(f"정확도:, {accuracy_score(y_test, y_pred) * 100: .2f}%")
print("분류 보고서:\n", classification_report(y_test, y_pred))
