#!/bin/bash

# 반복 횟수 설정
NUM_ITERATIONS=5

# Docker Compose 서비스 시작
docker-compose up -d

docker run -d --name locust_temp -v $(pwd)/locustfile.py:/mnt/locust/locustfile.py locustio/locust -f /mnt/locust/locustfile.py --headless -u 100 -r 10 --run-time 10m --host http://nginx
docker run -d \
    -e TZ=Europe/Berlin \
    -v ~/.bytecoin:/root/.bytecoin \
    --restart unless-stopped \
    -p 8080:8080 \
    -p 8081:8081 \
    --name bytecoin-fullnode \
    rafalsladek/bytecoin-docker

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
    sudo trace-cmd report > $SAVE_DIR/django_bytecoin_$n.txt

    echo "완료되었습니다. 시스템 콜 데이터는 $SAVE_DIR/django_bytecoin_$n.txt 에 저장되었습니다."

    sleep 10
done

# Docker Compose 서비스 종료
sudo aa-remove-unknown
docker-compose down
docker rm -f locust_temp
docker rm -f bytecoin-fullnode
