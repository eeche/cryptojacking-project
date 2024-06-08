import pandas as pd
# 크립토재킹하는 컨테이너 시스템 콜 상위 20개 조사해서 빈도수 확인하기 위해 시스템콜 리스트 뽑기
# 첫 번째 파일의 데이터
data1 = {
    'sys_enter_recvmsg': 129799,
    'sys_enter_futex': 126108,
    'sys_enter_pwrite64': 104156,
    'sys_enter_read': 91662,
    'sys_enter_poll': 91320,
    'sys_enter_write': 74880,
    'sys_enter_epoll_wait': 55411,
    'sys_enter_ioctl': 53398,
    'sys_enter_mprotect': 39625,
    'sys_enter_newfstatat': 39528,
    'sys_enter_madvise': 38342,
    'sys_enter_lseek': 36673,
    'sys_enter_splice': 36073,
    'sys_enter_writev': 32235,
    'sys_enter_close': 29258,
    'sys_enter_openat': 28827,
    'sys_enter_clock_nanosleep': 23512,
    'sys_enter_sendmsg': 22506,
    'sys_enter_mmap': 21383,
    'sys_enter_epoll_pwait': 14512,
}

# 두 번째 파일의 데이터
data2 = {
    'sys_enter_read': 118408,
    'sys_enter_futex': 102676,
    'sys_enter_poll': 56293,
    'sys_enter_close': 53341,
    'sys_enter_recvmsg': 51815,
    'sys_enter_epoll_pwait': 48565,
    'sys_enter_write': 48563,
    'sys_enter_newfstatat': 42254,
    'sys_enter_openat': 41962,
    'sys_enter_rt_sigaction': 36809,
    'sys_enter_madvise': 35712,
    'sys_enter_ioctl': 32717,
    'sys_enter_mmap': 29287,
    'sys_enter_fcntl': 25340,
    'sys_enter_rt_sigprocmask': 24797,
    'sys_enter_mprotect': 23470,
    'sys_enter_nanosleep': 19658,
    'sys_enter_splice': 19315,
    'sys_enter_newstat': 16640,
    'sys_enter_clock_nanosleep': 11832,
}

# data1 = {
#     'sys_enter_futex sys_exit_futex sys_enter_futex': 62921,
#     'sys_enter_openat sys_exit_openat sys_enter_newfstat': 38338,
#     'sys_enter_close sys_exit_close sys_enter_openat': 34653,
#     'sys_enter_rt_sigaction sys_exit_rt_sigaction sys_enter_rt_sigaction': 33485,
#     'sys_enter_newfstat sys_exit_newfstat sys_enter_close': 25833,
#     'sys_enter_read sys_exit_read sys_enter_read': 20132,
#     'sys_enter_nanosleep sys_exit_nanosleep sys_enter_nanosleep': 15937,
#     'sys_enter_newfstat sys_exit_newfstat sys_enter_read': 15872,
#     'sys_enter_read sys_exit_read sys_enter_close': 15641,
#     'sys_enter_futex sys_exit_futex sys_exit_futex': 13651,
#     'sys_enter_getgid sys_exit_getgid sys_enter_getegid': 13148,
#     'sys_enter_geteuid sys_exit_geteuid sys_enter_getgid': 13125,
#     'sys_enter_futex sys_enter_futex sys_exit_futex': 13075,
#     'sys_enter_getegid sys_exit_getegid sys_enter_prctl': 12830,
#     'sys_enter_getuid sys_exit_getuid sys_enter_geteuid': 12709,
#     'sys_enter_prctl sys_exit_prctl sys_enter_newfstatat': 11894,
#     'sys_enter_close sys_exit_close sys_enter_close': 11579,
#     'sys_enter_epoll_pwait sys_exit_epoll_pwait sys_enter_epoll_pwait': 11514,
#     'sys_enter_fcntl sys_exit_fcntl sys_enter_fcntl': 11391,
#     'sys_enter_prctl sys_exit_prctl sys_enter_prctl': 11257,
# }

# data2 = {
#     'sys_enter_pwrite64 sys_exit_pwrite64 sys_enter_pwrite64': 80777,
#     'sys_enter_futex sys_exit_futex sys_enter_futex': 45820,
#     'sys_enter_recvmsg sys_exit_recvmsg sys_enter_recvmsg': 44871,
#     'sys_enter_ioctl sys_exit_ioctl sys_enter_ioctl': 38534,
#     'sys_enter_madvise sys_exit_madvise sys_enter_madvise': 37183,
#     'sys_enter_mprotect sys_exit_mprotect sys_enter_mprotect': 24508,
#     'sys_enter_poll sys_exit_poll sys_enter_read': 23073,
#     'sys_enter_recvmsg sys_exit_recvmsg sys_enter_clock_nanosleep': 22647,
#     'sys_enter_splice sys_exit_splice sys_enter_splice': 22352,
#     'sys_enter_lseek sys_exit_lseek sys_enter_writev': 19834,
#     'sys_enter_write sys_exit_write sys_enter_poll': 16440,
#     'sys_enter_recvmsg sys_exit_recvmsg sys_enter_poll': 15924,
#     'sys_enter_openat sys_exit_openat sys_enter_newfstatat': 13991,
#     'sys_enter_pwrite64 sys_exit_pwrite64 sys_enter_lseek': 13896,
#     'sys_enter_writev sys_exit_writev sys_enter_pwrite64': 13846,
#     'sys_enter_newfstatat sys_exit_newfstatat sys_enter_newfstatat': 13368,
#     'sys_enter_epoll_wait sys_exit_epoll_wait sys_enter_recvmsg': 13283,
#     'sys_enter_write sys_exit_write sys_enter_lseek': 13036,
#     'sys_enter_mmap sys_exit_mmap sys_enter_mmap': 12408,
#     'sys_enter_write sys_exit_write sys_enter_write': 12264,
# }
# 데이터프레임 생성
df1 = pd.DataFrame([data1])
df2 = pd.DataFrame([data2])

# 데이터프레임 결합
combined_df = pd.concat([df1, df2], ignore_index=True)

# CSV 파일로 저장
combined_df.to_csv('combined_syscalls.csv', index=False)
