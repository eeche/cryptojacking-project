import re
import sys
import pandas as pd
import joblib
from collections import Counter

# 로그 파일 파싱 함수
def parse_log_file(file_path):
    syscall_pattern = re.compile(r'(.*)\[(\d+)\]\s+([\d.]+):\s+(\w+):\s+(.*)')
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            match = syscall_pattern.search(line)
            if match:
                process, cpu, timestamp, syscall, args = match.groups()
                if 'trace-cmd' not in process:
                    data.append(syscall)
    return data

# 시스템 호출 빈도 계산 함수
def enter_syscall_counter(data):
    sys_enter_data = [syscall for syscall in data if 'sys_enter_' in syscall]
    syscall_counter = Counter(sys_enter_data)
    sorted_syscalls = syscall_counter.most_common()
    return sorted_syscalls

# 빈도 데이터프레임 생성 함수
def create_frequency_dataframe(sorted_syscalls):
    df = pd.DataFrame(sorted_syscalls, columns=['syscall', 'count'])
    df = df.set_index('syscall').T
    return df

# 모델 예측 함수
def predict_with_model(df, model_path, scaler_path):
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    X = scaler.transform(df)
    predictions = model.predict(X)
    return predictions

# 메인 함수
if __name__ == "__main__":
    log_file_path = sys.argv[1]
    model_file_path = sys.argv[2]
    scaler_file_path = sys.argv[3]

    data = parse_log_file(log_file_path)
    sorted_syscalls = enter_syscall_counter(data)
    df = create_frequency_dataframe(sorted_syscalls)
    predictions = predict_with_model(df, model_file_path, scaler_file_path)
    
    print(f"Predictions: {predictions}")
