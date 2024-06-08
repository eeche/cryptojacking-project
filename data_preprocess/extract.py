import re
import os
from collections import Counter

# 파일 경로 목록
file_paths = {
    'normal': {'data_analyze_1.txt', 'django_1.txt', 'data_analyze_2.txt',
               },
    'abnormal': {'data_analyze_bytecoin_1.txt', 'django_byte_1.txt', 'data_analyze_bytecoin_2.txt',
                 }
}

syscall_pattern = re.compile(r'(.*)\[(\d+)\]\s+([\d.]+):\s+(\w+):\s+(.*)')


def parse_log_file(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            match = syscall_pattern.search(line)
            if match:
                process, cpu, timestamp, syscall, args = match.groups()
                if 'trace-cmd' not in process:
                    data.append((float(timestamp), syscall))
    return data


def save_split_files(data, output_dir, label, original_file_name):
    start_time = data[0][0]
    split_data = []
    split_index = 1

    for timestamp, syscall in data:
        if timestamp - start_time >= 6:
            split_file_name = f'{split_index}_{original_file_name}.txt'
            split_file_path = os.path.join(output_dir, split_file_name)
            analyze_split_file(split_data, split_file_path, label)
            split_data = []
            start_time = timestamp
            split_index += 1
            print(f'Saved and analyzed split file: {split_file_path}')

        split_data.append((timestamp, syscall))


def analyze_split_file(split_data, split_file_path, label):
    base_file_path = split_file_path.rsplit('.', 1)[0]
    enter_syscall_counter(split_data, base_file_path, label)


def enter_syscall_counter(data, base_file_path, label):
    sys_enter_data = [syscall for _,
                      syscall in data if 'sys_enter_' in syscall]
    syscall_counter = Counter(sys_enter_data)
    sorted_syscalls = syscall_counter.most_common()
    with open(f'{base_file_path}_{label}_frequency.txt', 'w') as file:
        for syscall, count in sorted_syscalls:
            file.write(f'{syscall}: {count}\n')


def process_files(file_paths):
    for label, paths in file_paths.items():
        output_dir = label
        os.makedirs(output_dir, exist_ok=True)
        for path in paths:
            print(f'Processing file: {path}')
            data = parse_log_file(path)
            original_file_name = os.path.basename(path).rsplit('.', 1)[0]
            save_split_files(data, output_dir, label, original_file_name)
            print(f'Completed processing for file: {path}')


process_files(file_paths)
