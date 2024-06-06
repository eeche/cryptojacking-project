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
    return top_features, df

# 개별 파일 처리 및 데이터 준비 함수
def prepare_individual_data(paths, label, top_n=30, is_3gram=False):
    all_data = []
    original_data = {}
    for file in paths:
        top_features, full_data = extract_top_features(file, top_n=top_n, is_3gram=is_3gram)
        top_features['label'] = label
        top_features['file'] = file
        all_data.append(top_features)
        original_data[file] = full_data
    return pd.concat(all_data, ignore_index=True), original_data

# 정상 및 비정상 데이터 준비
normal_freq_data, normal_freq_full = prepare_individual_data(file_paths['normal']['frequency'], label='normal')
normal_gram_data, normal_gram_full = prepare_individual_data(file_paths['normal']['3gram_frequency'], label='normal', is_3gram=True)
abnormal_freq_data, abnormal_freq_full = prepare_individual_data(file_paths['abnormal']['frequency'], label='abnormal')
abnormal_gram_data, abnormal_gram_full = prepare_individual_data(file_paths['abnormal']['3gram_frequency'], label='abnormal', is_3gram=True)

# 데이터 통합
all_freq_data = pd.concat([normal_freq_data, abnormal_freq_data], ignore_index=True)
all_gram_data = pd.concat([normal_gram_data, abnormal_gram_data], ignore_index=True)
full_data = {**normal_freq_full, **normal_gram_full, **abnormal_freq_full, **abnormal_gram_full}

# 피처 벡터 생성 함수
def create_feature_vector(df):
    feature_vector = df.pivot_table(index='file', columns='feature', values='frequency', fill_value=0)
    feature_vector['label'] = df.groupby('file')['label'].first()
    return feature_vector

# 피처 벡터 생성
X_freq = create_feature_vector(all_freq_data)
X_gram = create_feature_vector(all_gram_data)

# 데이터 확인 및 0 값 수정
def correct_zeros(df, original_data):
    for index, row in df.iterrows():
        file = row.name
        if file in original_data:
            original_file_data = original_data[file]
            for feature in df.columns:
                if feature != 'label' and df.at[index, feature] == 0:
                    if feature in original_file_data['feature'].values:
                        actual_value = original_file_data[original_file_data['feature'] == feature]['frequency'].values[0]
                        df.at[index, feature] = actual_value
    return df

X_freq_corrected = correct_zeros(X_freq, full_data)
X_gram_corrected = correct_zeros(X_gram, full_data)

# 데이터 확인
print(X_freq_corrected.head())
print(X_gram_corrected.head())

# 데이터 파일로 저장
X_freq_corrected.to_csv('top_30_frequency_features_corrected.csv', index=False)
X_gram_corrected.to_csv('top_30_3gram_features_corrected.csv', index=False)