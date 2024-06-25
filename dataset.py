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

# 데이터프레임 생성
df1 = pd.DataFrame([data1])
df2 = pd.DataFrame([data2])

# 데이터프레임 결합
combined_df = pd.concat([df1, df2], ignore_index=True)

# CSV 파일로 저장
combined_df.to_csv('combined_syscalls.csv', index=False)
