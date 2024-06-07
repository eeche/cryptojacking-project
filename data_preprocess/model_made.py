import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import VotingClassifier, RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
import xgboost as xgb
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# 데이터 로드
file_path = 'C:\\Users\\dlckd\\Desktop\\cryptoProject\\data_preprocess\\new_frequency_features_corrected.csv'
data = pd.read_csv(file_path)

# 데이터 분리
X = data.drop(columns=['label'])
y = data['label']

# 특징의 최대 길이를 60으로 제한
if X.shape[1] > 60:
    X = X.iloc[:, :60]

# 학습용과 테스트용 데이터셋으로 분리
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# 스케일링
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 스케일링 후 데이터 형태 출력
print("Scaled X_train shape:", X_train.shape)
print("Scaled X_test shape:", X_test.shape)
print("First 5 rows of scaled X_train:\n", X_train[:5])

# 모델 정의
gnb = GaussianNB()
knn = KNeighborsClassifier()
lr = LogisticRegression()
svm = SVC(probability=True)
rf = RandomForestClassifier()
gb = GradientBoostingClassifier()
xgb_clf = xgb.XGBClassifier(use_label_encoder=False, eval_metric='mlogloss')
ada = AdaBoostClassifier()
lgbm = LGBMClassifier()
catboost = CatBoostClassifier(verbose=0)

# 모델 학습 및 평가 함수


def train_and_evaluate(models, X_train, X_test, y_train, y_test):
    results = {}
    for name, model in models:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        results[name] = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': classification_report(y_test, y_pred, output_dict=True)['weighted avg']['precision'],
            'recall': classification_report(y_test, y_pred, output_dict=True)['weighted avg']['recall'],
            'f1-score': classification_report(y_test, y_pred, output_dict=True)['weighted avg']['f1-score']
        }
    return results


# 개별 모델 학습 및 평가
models = [
    ('GNB', gnb), ('KNN', knn), ('LR', lr), ('SVM', svm),
    ('RF', rf), ('GB', gb), ('XGB', xgb_clf), ('AdaBoost', ada),
    ('LightGBM', lgbm), ('CatBoost', catboost)
]
results_freq = train_and_evaluate(models, X_train, X_test, y_train, y_test)

# Voting Classifier 정의 및 평가 (soft voting)
voting_clf = VotingClassifier(estimators=[(
    'GNB', gnb), ('LR', lr), ('RF', rf), ('XGB', xgb_clf)], voting='soft')
voting_clf.fit(X_train, y_train)
y_pred_voting = voting_clf.predict(X_test)
results_freq['Voting'] = {
    'accuracy': accuracy_score(y_test, y_pred_voting),
    'precision': classification_report(y_test, y_pred_voting, output_dict=True)['weighted avg']['precision'],
    'recall': classification_report(y_test, y_pred_voting, output_dict=True)['weighted avg']['recall'],
    'f1-score': classification_report(y_test, y_pred_voting, output_dict=True)['weighted avg']['f1-score']
}

# 결과 출력
print("Frequency Results:", results_freq)

# 결과 표로 정리
results_freq_df = pd.DataFrame(results_freq).T
results_freq_df.loc['Avg.'] = results_freq_df.mean()
print(results_freq_df)

# 결과 파일로 저장
results_freq_df.to_csv('model_results.csv')

# 모델 저장
joblib.dump(voting_clf, 'voting_classifier_model.pkl')
joblib.dump(scaler, 'scaler.pkl')
