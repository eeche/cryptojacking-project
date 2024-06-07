import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import pandas as pd

# data_path = 'new_frequency_features_corrected.csv'
data_path = 'C:\\Users\\dlckd\\Desktop\\cryptoProject\\merged.csv'

data = pd.read_csv(data_path)

X = data.iloc[:, :-1]
y = data.iloc[:, -1]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

random_forest_model = RandomForestClassifier(n_estimators=10, random_state=42)
random_forest_model.fit(X_train, y_train)
joblib.dump(random_forest_model, 'random_forest_model.pkl')
model_loaded = joblib.load('random_forest_model.pkl')

y_pred = model_loaded.predict(X_test)

print(f"정확도:, {accuracy_score(y_test, y_pred) * 100: .2f}%")
print("분류 보고서:\n", classification_report(y_test, y_pred))
