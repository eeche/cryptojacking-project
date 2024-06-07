import re
import os
from collections import Counter

# 파일 경로 목록
file_paths = {
    'normal': {
        'dap_1.txt',
        'dap_2.txt',
        'dp_1.txt',
        'dp_2.txt',
        'ep_1.txt',
        'ep_2.txt',
    },
    'abnormal': {
        'dapb_1.txt',
        'dapb_2.txt',
        'dpb_1.txt',
        'dpb_2.txt',
        'epb_1.txt',
        'epb_2.txt',
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

def save_split_files(data, output_dir, label):
    start_time = data[0][0]
    split_data = []
    split_index = 0

    for timestamp, syscall in data:
        if timestamp - start_time >= 6:
            split_file_path = os.path.join(output_dir, f'part{split_index}.txt')
            with open(split_file_path, 'w') as file:
                for _, sys in split_data:
                    file.write(f'{sys}\n')
            analyze_split_file(split_data, split_file_path, label)
            split_data = []
            start_time = timestamp
            split_index += 1
            print(f'Saved and analyzed split file: {split_file_path}')

        split_data.append((timestamp, syscall))
    
    # Save and analyze the remaining data
    if split_data:
        split_file_path = os.path.join(output_dir, f'part{split_index}.txt')
        with open(split_file_path, 'w') as file:
            for _, sys in split_data:
                file.write(f'{sys}\n')
        analyze_split_file(split_data, split_file_path, label)
        print(f'Saved and analyzed split file: {split_file_path}')

def analyze_split_file(split_data, split_file_path, label):
    base_file_path = split_file_path.rsplit('.', 1)[0]
    enter_syscall_counter(split_data, base_file_path, label)
    save_3gram_frequencies(split_data, base_file_path, label)

def enter_syscall_counter(data, base_file_path, label):
    sys_enter_data = [syscall for _, syscall in data if 'sys_enter_' in syscall]
    syscall_counter = Counter(sys_enter_data)
    sorted_syscalls = syscall_counter.most_common()
    with open(f'{base_file_path}_{label}_frequency.txt', 'w') as file:
        for syscall, count in sorted_syscalls:
            file.write(f'{syscall}: {count}\n')

def generate_3grams(data):
    n = 3
    syscalls = [syscall for _, syscall in data]
    return [tuple(syscalls[i:i+n]) for i in range(len(syscalls)-n+1)]

def save_3gram_frequencies(data, base_file_path, label):
    three_grams = generate_3grams(data)
    three_gram_counter = Counter(three_grams)
    sorted_three_grams = three_gram_counter.most_common()
    with open(f'{base_file_path}_{label}_3gram_frequency.txt', 'w', encoding='utf-8') as file:
        for three_gram, count in sorted_three_grams:
            three_gram_str = ' '.join(three_gram)
            file.write(f'{three_gram_str}: {count}\n')

def process_files(file_paths):
    for label, paths in file_paths.items():
        for path in paths:
            print(f'Processing file: {path}')
            data = parse_log_file(path)
            base_file_name = os.path.basename(path).rsplit('.', 1)[0]
            output_dir = os.path.join(base_file_name, label)
            os.makedirs(output_dir, exist_ok=True)
            save_split_files(data, output_dir, label)
            print(f'Completed processing for file: {path}')

process_files(file_paths)
