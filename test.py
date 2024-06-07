import re
from collections import Counter

# 로그 파일 파싱 함수
file_path = 'C:\\Users\\dlckd\\Desktop\\cryptoProject\\Data\\crypto\\bytecoin.txt'
syscall_pattern = re.compile(r'(.*)\[(\d+)\]\s+([\d.]+):\s+(\w+):\s+(.*)')


def parse_log_file(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            match = syscall_pattern.search(line)
            if match:
                process, cpu, timestamp, syscall, args = match.groups()
                if 'trace-cmd' not in process:
                    data.append(syscall)
    return data


def enter_syscall_counter(data):
    sys_enter_data = [syscall for syscall in data if 'sys_enter_' in syscall]
    syscall_counter = Counter(sys_enter_data)
    sorted_syscalls = syscall_counter.most_common()
    base_file_path = file_path.rsplit('.', 1)[0]
    with open(f'{base_file_path}_frequency.txt', 'w') as file:
        for syscall, count in sorted_syscalls:
            file.write(f'{syscall}: {count}\n')


def generate_3grams(data):
    n = 3
    return [tuple(data[i:i+n]) for i in range(len(data)-n+1)]


def save_3grams_to_file(data):
    three_grams = generate_3grams(data)
    base_file_path = file_path.rsplit('.', 1)[0]
    with open(f'{base_file_path}_3grams.txt', 'w', encoding='utf-8') as file:
        for three_gram in three_grams:
            three_gram_str = ' '.join(three_gram)
            file.write(f'{three_gram_str}\n')


def save_3gram_frequencies(data):
    three_grams = generate_3grams(data)
    three_gram_counter = Counter(three_grams)
    sorted_three_grams = three_gram_counter.most_common()
    base_file_path = file_path.rsplit('.', 1)[0]
    with open(f'{base_file_path}_3gram_frequency.txt', 'w', encoding='utf-8') as file:
        for three_gram, count in sorted_three_grams:
            three_gram_str = ' '.join(three_gram)
            file.write(f'{three_gram_str}: {count}\n')


data = parse_log_file(file_path)
enter_syscall_counter(data)
save_3grams_to_file(data)
save_3gram_frequencies(data)
