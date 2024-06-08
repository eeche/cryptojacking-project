#!/bin/bash

# 반복 횟수 설정
NUM_ITERATIONS=5

# Docker Compose 서비스 시작
docker-compose up -d locust

sleep 100

# 데이터 저장 디렉토리 설정
SAVE_DIR=~/Desktop/syscall
mkdir -p $SAVE_DIR

for ((n=1; n<=NUM_ITERATIONS; n++))
do
    # 시스템 콜 기록 시작
    sudo trace-cmd record -e syscalls &
    TRACE_CMD_PID=$!

    # 10분 동안 대기
    sleep 600

    # trace-cmd 종료
    sudo kill -SIGINT $TRACE_CMD_PID
    sleep 5
    # 보고서 생성 및 저장
    sudo trace-cmd report > $SAVE_DIR/ecommerce_$n.txt

    echo "완료되었습니다. 시스템 콜 데이터는 $SAVE_DIR/ecommerce_$n.txt 에 저장되었습니다."

    sleep 10
done

# Docker Compose 서비스 종료
sudo aa-remove-unknown
docker-compose down
