file_path = 'C:\\Users\\dlckd\\Desktop\\cryptoProject\\Data\\crypto\\bitcore_3gram_frequency.txt'
output_file_path = 'filtered_sys_enter_lines.txt'

keywords = [
    "sys_enter_recvmsg", "sys_enter_futex", "sys_enter_pwrite64", "sys_enter_read",
    "sys_enter_poll", "sys_enter_write", "sys_enter_epoll_wait", "sys_enter_ioctl",
    "sys_enter_mprotect", "sys_enter_newfstatat", "sys_enter_madvise", "sys_enter_lseek",
    "sys_enter_splice", "sys_enter_writev", "sys_enter_close", "sys_enter_openat",
    "sys_enter_clock_nanosleep", "sys_enter_sendmsg", "sys_enter_mmap", "sys_enter_epoll_pwait",
    "sys_enter_newfstat", "sys_enter_nanosleep", "sys_enter_rt_sigaction", "sys_enter_getrandom",
    "sys_enter_prctl", "sys_enter_readlink", "sys_enter_fcntl", "sys_enter_geteuid",
    "sys_enter_getuid", "sys_enter_getegid"
]

with open(file_path, 'r', encoding='utf-8') as infile, open(output_file_path, 'w', encoding='utf-8') as outfile:
    for line in infile:
        if line.startswith('sys_enter_'):
            if any(keyword in line for keyword in keywords):
                outfile.write(line)

print(f"'sys_enter_'로 시작하는 모든 줄이 {output_file_path}에 저장되었습니다.")
