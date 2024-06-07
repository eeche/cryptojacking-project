import re
import sys
import pandas as pd
import joblib
from collections import Counter
from datetime import datetime, timedelta
import numpy as np

# 추출할 시스템 콜 목록
target_syscalls = [
    "sys_enter_clock_nanosleep", "sys_enter_close", "sys_enter_epoll_pwait", "sys_enter_epoll_wait", "sys_enter_fcntl",
    "sys_enter_futex", "sys_enter_getegid", "sys_enter_geteuid", "sys_enter_getrandom", "sys_enter_getuid",
    "sys_enter_ioctl", "sys_enter_lseek", "sys_enter_madvise", "sys_enter_mmap", "sys_enter_mprotect",
    "sys_enter_nanosleep", "sys_enter_newfstat", "sys_enter_newfstatat", "sys_enter_openat", "sys_enter_poll",
    "sys_enter_prctl", "sys_enter_pwrite64", "sys_enter_read", "sys_enter_readlink", "sys_enter_recvmsg",
    "sys_enter_rt_sigaction", "sys_enter_sendmsg", "sys_enter_splice", "sys_enter_write", "sys_enter_writev"
]

# 로그 파일 파싱 함수
def parse_log_file(file_path):
    syscall_pattern = re.compile(r'(.*)\[(\d+)\]\s+([\d.]+):\s+(\w+):\s+(.*)')
    data = []
    with open(file_path, 'r', encoding='latin1') as file:  # latin1 인코딩으로 파일 읽기
        for line in file:
            match = syscall_pattern.search(line)
            if match:
                process, cpu, timestamp, syscall, args = match.groups()
                if 'trace-cmd' not in process:
                    timestamp = float(timestamp)  # 타임스탬프를 float으로 변환
                    data.append((timestamp, syscall))
    return data

# 6초 단위로 데이터 나누기
def split_data_by_time(data, interval=6):
    data.sort(key=lambda x: x[0])  # 타임스탬프로 정렬
    start_time = data[0][0]
    end_time = start_time + interval
    split_data = []
    current_interval_data = []

    for timestamp, syscall in data:
        if timestamp < end_time:
            current_interval_data.append(syscall)
        else:
            split_data.append(current_interval_data)
            current_interval_data = [syscall]
            start_time = timestamp
            end_time = start_time + interval

    if current_interval_data:
        split_data.append(current_interval_data)

    return split_data

# 시스템 호출 빈도 계산 함수
def enter_syscall_counter(data, target_features):
    sys_enter_data = [syscall for syscall in data if 'sys_enter_' in syscall]
    syscall_counter = Counter(sys_enter_data)
    sorted_syscalls = {syscall: syscall_counter[syscall] for syscall in target_features if syscall in syscall_counter}
    return sorted_syscalls

# 빈도 데이터프레임 생성 함수
def create_frequency_dataframe(syscall_counts_list, target_features):
    df_dict = {feature: [] for feature in target_features}
    for syscall_counts in syscall_counts_list:
        for feature in target_features:
            df_dict[feature].append(syscall_counts.get(feature, 0))
    df = pd.DataFrame(df_dict)
    return df

# 모델 예측 함수
def predict_with_model(df, model_path, scaler_path):
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    X = scaler.transform(df)
    predictions = model.predict(X)
    return predictions, X

# 과반수 예측값 및 비율 계산 함수
def majority_vote(predictions):
    count = Counter(predictions)
    majority_value, majority_count = count.most_common(1)[0]
    total_count = len(predictions)
    majority_percentage = (majority_count / total_count) * 100
    return majority_value, majority_percentage

# 메인 함수
if __name__ == "__main__":
    log_file_path = sys.argv[1]
    model_file_path = sys.argv[2]
    scaler_file_path = sys.argv[3]

    # 로그 파일 파싱
    data = parse_log_file(log_file_path)
    
    # 6초 단위로 데이터 나누기
    split_data = split_data_by_time(data, interval=6)
    
    # 빈도 데이터프레임 생성
    syscall_counts_list = [enter_syscall_counter(interval_data, target_syscalls) for interval_data in split_data]
    df = create_frequency_dataframe(syscall_counts_list, target_syscalls)
    
    # 스케일러 적용 전 데이터프레임 출력
    print("Dataframe before scaling:")
    print(df)
    
    # 모델 예측
    predictions, scaled_df = predict_with_model(df, model_file_path, scaler_file_path)
    
    # 스케일러 적용 후 데이터프레임 출력
    print("Dataframe after scaling:")
    print(scaled_df)
    
    # 과반수 예측값 및 비율 계산
    majority_value, majority_percentage = majority_vote(predictions)
    
    # 예측 결과의 분포 출력
    prediction_counts = Counter(predictions)
    print(f"Prediction distribution: {prediction_counts}")
    
    # 결과 출력
    print(f"Predictions: {predictions}")
    print(f"Majority Prediction: {majority_value} ({majority_percentage:.2f}%)")
