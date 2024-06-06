import pandas as pd

# 파일 경로
file_paths = {
    'normal': {
        'frequency': [
            'blockchain.txt_frequency.txt',
            'blog.txt_frequency.txt',
            'car.txt_frequency.txt',
            'iot.txt_frequency.txt',
            'mobilegame.txt_frequency.txt',
            'splunk.txt_frequency.txt',
        ],
        '3gram_frequency': [
            'blockchain.txt_3gram_frequency.txt',
            'blog.txt_3gram_frequency.txt',
            'car.txt_3gram_frequency.txt',
            'iot.txt_3gram_frequency.txt',
            'mobilegame.txt_3gram_frequency.txt',
            'splunk.txt_3gram_frequency.txt'
        ]
    },
    'abnormal': {
        'frequency': [
            'bitcore.txt_frequency.txt',
            'blockchain_bitcore.txt_frequency.txt',
            'blog_bitcore.txt_frequency.txt',
            'car_bitcore.txt_frequency.txt',
            'iot_bitcore.txt_frequency.txt',
            'mobilegame_bitcore.txt_frequency.txt',
            'splunk_bitcore.txt_frequency.txt',
        ],
        '3gram_frequency': [
            'bitcore.txt_3gram_frequency.txt',
            'blockchain_bitcore.txt_3gram_frequency.txt',
            'blog_bitcore.txt_3gram_frequency.txt',
            'car_bitcore.txt_3gram_frequency.txt',
            'iot_bitcore.txt_3gram_frequency.txt',
            'mobilegame_bitcore.txt_3gram_frequency.txt',
            'splunk_bitcore.txt_3gram_frequency.txt'
        ]
    }
}
# 상위 30개 특징 추출 함수
def extract_top_features(file_path, top_n=30, is_3gram=False):
    if is_3gram:
        df = pd.read_csv(file_path, sep=':', header=None, names=['feature', 'frequency'], engine='python')
        df['feature'] = df['feature'].str.strip()
    else:
        df = pd.read_csv(file_path, sep=' ', header=None, names=['feature', 'frequency'])
    top_features = df.nlargest(top_n, 'frequency')
    return top_features

# 개별 파일 처리 및 데이터 준비 함수
def prepare_individual_data(paths, label, top_n=30, is_3gram=False):
    all_data = []
    for file in paths:
        data = extract_top_features(file, top_n=top_n, is_3gram=is_3gram)
        data['label'] = label
        data['file'] = file
        all_data.append(data)
    return pd.concat(all_data, ignore_index=True)

# 정상 및 비정상 데이터 준비
normal_freq_data = prepare_individual_data(file_paths['normal']['frequency'], label='normal')
normal_gram_data = prepare_individual_data(file_paths['normal']['3gram_frequency'], label='normal', is_3gram=True)
abnormal_freq_data = prepare_individual_data(file_paths['abnormal']['frequency'], label='abnormal')
abnormal_gram_data = prepare_individual_data(file_paths['abnormal']['3gram_frequency'], label='abnormal', is_3gram=True)

# 데이터 통합
all_freq_data = pd.concat([normal_freq_data, abnormal_freq_data], ignore_index=True)
all_gram_data = pd.concat([normal_gram_data, abnormal_gram_data], ignore_index=True)

# 피처 벡터 생성 함수
def create_feature_vector(df):
    feature_vector = df.pivot_table(index='file', columns='feature', values='frequency', fill_value=0)
    feature_vector['label'] = df.groupby('file')['label'].first()
    return feature_vector

# 피처 벡터 생성
X_freq = create_feature_vector(all_freq_data)
X_gram = create_feature_vector(all_gram_data)

# 데이터 확인
print(X_freq.head())
print(X_gram.head())

# 데이터 파일로 저장
X_freq.to_csv('top_30_frequency_features.csv', index=False)
X_gram.to_csv('top_30_3gram_features.csv', index=False)