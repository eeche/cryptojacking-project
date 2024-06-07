import re
import sys
import pandas as pd
import joblib
from collections import Counter

# 추출할 시스템 콜 목록
target_syscalls = [
    "sys_enter_recvmsg", "sys_enter_futex", "sys_enter_pwrite64", "sys_enter_read", "sys_enter_poll",
    "sys_enter_write", "sys_enter_epoll_wait", "sys_enter_ioctl", "sys_enter_mprotect", "sys_enter_newfstatat",
    "sys_enter_madvise", "sys_enter_lseek", "sys_enter_splice", "sys_enter_writev", "sys_enter_close",
    "sys_enter_openat", "sys_enter_clock_nanosleep", "sys_enter_sendmsg", "sys_enter_mmap", "sys_enter_epoll_pwait",
    "sys_enter_newfstat", "sys_enter_nanosleep", "sys_enter_rt_sigaction", "sys_enter_getrandom", "sys_enter_prctl",
    "sys_enter_readlink", "sys_enter_fcntl", "sys_enter_geteuid", "sys_enter_getuid", "sys_enter_getegid"
]

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
def enter_syscall_counter(data, target_features):
    sys_enter_data = [syscall for syscall in data if 'sys_enter_' in syscall]
    syscall_counter = Counter(sys_enter_data)
    sorted_syscalls = {syscall: syscall_counter[syscall] for syscall in target_features if syscall in syscall_counter}
    return sorted_syscalls

# 빈도 데이터프레임 생성 함수
def create_frequency_dataframe(syscall_counts):
    df = pd.DataFrame.from_dict(syscall_counts, orient='index', columns=['count'])
    df = df.T  # Transpose to have features as columns
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
    frequency_file_path = sys.argv[4]

    data = parse_log_file(log_file_path)
    syscall_counts = enter_syscall_counter(data, target_syscalls)
    df = create_frequency_dataframe(syscall_counts)
    
    # 모델 예측
    predictions = predict_with_model(df, model_file_path, scaler_file_path)
    
    # 빈도 파일 저장
    df.to_csv(frequency_file_path, index=False)

    print(f"Predictions: {predictions}")
