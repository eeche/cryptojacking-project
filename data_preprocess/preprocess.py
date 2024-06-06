import os
import pandas as pd

# 파일 경로 목록
file_dirs = {
    'normal': {
        'frequency': [
            'blockchain/normal',
            'blog/normal',
            'car/normal',
            'iot/normal',
            'mobilegame/normal',
            'splunk/normal',
            'dap_1/normal',
            'dap_2/normal',
            'dp_1/normal',
            'dp_2/normal',
            'ep_1/normal',
            'ep_2/normal',
        ],
        '3gram_frequency': [
            'blockchain/normal',
            'blog/normal',
            'car/normal',
            'iot/normal',
            'mobilegame/normal',
            'splunk/normal',
            'dap_1/normal',
            'dap_2/normal',
            'dp_1/normal',
            'dp_2/normal',
            'ep_1/normal',
            'ep_2/normal',
        ]
    },
    'abnormal': {
        'frequency': [
            'blockchain/abnormal',
            'blog/abnormal',
            'car/abnormal',
            'iot/abnormal',
            'mobilegame/abnormal',
            'splunk/abnormal',
            'dap_1/abnormal',
            'dap_2/abnormal',
            'dp_1/abnormal',
            'dp_2/abnormal',
            'ep_1/abnormal',
            'ep_2/abnormal',
        ],
        '3gram_frequency': [
            'blockchain/abnormal',
            'blog/abnormal',
            'car/abnormal',
            'iot/abnormal',
            'mobilegame/abnormal',
            'splunk/abnormal',
            'dap_1/abnormal',
            'dap_2/abnormal',
            'dp_1/abnormal',
            'dp_2/abnormal',
            'ep_1/abnormal',
            'ep_2/abnormal',
        ]
    }
}

# 추출할 시스템 콜 목록
target_syscalls = [
    "sys_enter_recvmsg", "sys_enter_futex", "sys_enter_pwrite64", "sys_enter_read", "sys_enter_poll",
    "sys_enter_write", "sys_enter_epoll_wait", "sys_enter_ioctl", "sys_enter_mprotect", "sys_enter_newfstatat",
    "sys_enter_madvise", "sys_enter_lseek", "sys_enter_splice", "sys_enter_writev", "sys_enter_close",
    "sys_enter_openat", "sys_enter_clock_nanosleep", "sys_enter_sendmsg", "sys_enter_mmap", "sys_enter_epoll_pwait",
    "sys_enter_newfstat", "sys_enter_nanosleep", "sys_enter_rt_sigaction", "sys_enter_getrandom", "sys_enter_prctl",
    "sys_enter_readlink", "sys_enter_fcntl", "sys_enter_geteuid", "sys_enter_getuid", "sys_enter_getegid"
]


def get_file_list(directory, suffix):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(suffix):
                file_list.append(os.path.join(root, file))
    return file_list

# 특정 특징 추출 함수


def extract_target_features(file_path, target_features, is_3gram=False):
    if is_3gram:
        df = pd.read_csv(file_path, sep=':', header=None, names=[
                         'feature', 'frequency'], engine='python')
        df['feature'] = df['feature'].str.strip()
    else:
        df = pd.read_csv(file_path, sep=':', header=None,
                         names=['feature', 'frequency'])
    filtered_features = df[df['feature'].isin(target_features)]
    return filtered_features, df

# 개별 파일 처리 및 데이터 준비 함수


def prepare_individual_data(dirs, label, target_features, is_3gram=False):
    all_data = []
    original_data = {}
    suffix = '_3gram_frequency.txt' if is_3gram else '_frequency.txt'
    for directory in dirs:
        files = get_file_list(directory, suffix)
        for file in files:
            print(f'Processing file: {file}')
            target_feature_data, full_data = extract_target_features(
                file, target_features, is_3gram=is_3gram)
            target_feature_data['label'] = label
            target_feature_data['file'] = file
            all_data.append(target_feature_data)
            original_data[file] = full_data
    return pd.concat(all_data, ignore_index=True), original_data


# 정상 및 비정상 데이터 준비
print('Preparing normal frequency data...')
normal_freq_data, normal_freq_full = prepare_individual_data(
    file_dirs['normal']['frequency'], label=0, target_features=target_syscalls)
print('Preparing abnormal frequency data...')
abnormal_freq_data, abnormal_freq_full = prepare_individual_data(
    file_dirs['abnormal']['frequency'], label=1, target_features=target_syscalls)

# 데이터 통합
print('Combining frequency data...')
all_freq_data = pd.concat(
    [normal_freq_data, abnormal_freq_data], ignore_index=True)
full_data = {**normal_freq_full, **abnormal_freq_full}

# 피처 벡터 생성 함수


def create_feature_vector(df):
    print('Creating feature vector...')
    feature_vector = df.pivot_table(
        index='file', columns='feature', values='frequency', fill_value=0)
    feature_vector['label'] = df.groupby('file')['label'].first()
    return feature_vector


# 피처 벡터 생성
X_freq = create_feature_vector(all_freq_data)

# 데이터 확인 및 0 값 수정


def correct_zeros(df, original_data):
    print('Correcting zero values in feature vector...')
    for index, row in df.iterrows():
        file = row.name
        if file in original_data:
            original_file_data = original_data[file]
            for feature in df.columns:
                if feature != 'label' and df.at[index, feature] == 0:
                    if feature in original_file_data['feature'].values:
                        actual_value = original_file_data[original_file_data['feature']
                                                          == feature]['frequency'].values[0]
                        df.at[index, feature] = actual_value
    return df


X_freq_corrected = correct_zeros(X_freq, full_data)

# 데이터 확인
print('Final feature vector:')
print(X_freq_corrected.head())

# 데이터 파일로 저장
print('Saving corrected feature vector to CSV...')
X_freq_corrected.to_csv('new_frequency_features_corrected.csv', index=False)
print('Process completed.')
