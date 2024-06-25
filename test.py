import re
from collections import Counter

# 로그 파일 파싱 함수
file_path = './Data/blog_1.txt'
syscall_pattern = re.compile(r'(.*)\[(\d+)\]\s+([\d.]+):\s+(\w+):\s+(.*)')


def parse_log_file(file_path):
    data = []
    processes = []
    with open(file_path, 'r') as file:
        for line in file:
            match = syscall_pattern.search(line)
            if match:
                process, cpu, timestamp, syscall, args = match.groups()
                if 'trace-cmd' not in process:
                    data.append(syscall)
                    processes.append(process)
    return data, processes


def enter_syscall_counter(data):
    sys_enter_data = [syscall for syscall in data if 'sys_enter_' in syscall]
    syscall_counter = Counter(sys_enter_data)
    sorted_syscalls = syscall_counter.most_common()
    base_file_path = file_path.rsplit('.', 1)[0]
    with open(f'{base_file_path}_frequency.txt', 'w') as file:
        for syscall, count in sorted_syscalls:
            file.write(f'{syscall}: {count}\n')


def process_counter(processes):
    process_counter = Counter(processes)
    sorted_processes = process_counter.most_common()
    base_file_path = file_path.rsplit('.', 1)[0]
    with open(f'{base_file_path}_process_frequency.txt', 'w') as file:
        for process, count in sorted_processes:
            file.write(f'{process}: {count}\n')


data, processes = parse_log_file(file_path)
enter_syscall_counter(data)
process_counter(processes)
