import pandas as pd
# 크립토재킹하는 컨테이너 시스템 콜 상위 20개 조사해서 빈도수 확인하기 위해 시스템콜 리스트 뽑기
# 첫 번째 파일의 데이터
bytecoin = {
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
    'sys_enter_epoll_pwait': 14512
}

# 두 번째 파일의 데이터
dashcoin = {
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
    'sys_enter_clock_nanosleep': 11832
}

dogecoin = {
    'sys_enter_times': 52256,
    'sys_enter_ioctl': 43440,
    'sys_enter_epoll_pwait': 21573,
    'sys_enter_poll': 15540,
    'sys_enter_read': 14222,
    'sys_enter_recvmsg': 13918,
    'sys_enter_futex': 13116,
    'sys_enter_newfstatat': 8174,
    'sys_enter_close': 7935,
    'sys_enter_openat': 6453,
    'sys_enter_inotify_add_watch': 5700,
    'sys_enter_nanosleep': 4377,
    'sys_enter_epoll_wait': 3822,
    'sys_enter_gettid': 3223,
    'sys_enter_timerfd_settime': 2839,
    'sys_enter_readlink': 2186,
    'sys_enter_madvise': 2010,
    'sys_enter_socket': 1583,
    'sys_enter_sched_yield': 1481,
    'sys_enter_write': 1310,
}


# 데이터프레임 생성
df1 = pd.DataFrame([bytecoin])
df2 = pd.DataFrame([dashcoin])
df3 = pd.DataFrame([dogecoin])

# 데이터프레임 결합
combined_df = pd.concat([df1, df2, df3], ignore_index=True)

# CSV 파일로 저장
combined_df.to_csv('combined_syscalls.csv', index=False)
