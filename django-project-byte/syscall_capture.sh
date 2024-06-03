#!/bin/bash

# Docker Compose로 주요 컨테이너 실행
docker-compose up -d

# Locust 트래픽 생성 및 시스템 콜 캡처를 백그라운드에서 시작
docker run -d --name locust_temp -v $(pwd)/locustfile.py:/mnt/locust/locustfile.py locustio/locust -f /mnt/locust/locustfile.py --headless -u 100 -r 10 --run-time 10m --host http://nginx
docker run -d \
    -e TZ=Europe/Berlin \
    -v ~/.bytecoin:/root/.bytecoin \
    --restart unless-stopped \
    -p 8080:8080 \
    -p 8081:8081 \
    --name bytecoin-fullnode \
    rafalsladek/bytecoin-docker

# 시스템 콜 캡처 시작
sudo trace-cmd record -e syscalls &
TRACE_CMD_PID=$!

# Locust 트래픽 생성 종료 대기 (10분)
sleep 600

# 시스템 콜 캡처 중지
sudo kill -SIGINT $TRACE_CMD_PID

# Docker Compose 및 Locust 컨테이너 정리
docker-compose down
docker rm -f locust_temp
docker rm -f bytecoin-fullnode

sudo trace-cmd report > trace.txt
echo "완료되었습니다. 시스템 콜 데이터는 trace.txt 에 저장되었습니다."
