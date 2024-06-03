#!/bin/bash

docker-compose up -d locust

docker run -d \
    -e TZ=Europe/Berlin \
    -v ~/.bytecoin:/root/.bytecoin \
    --restart unless-stopped \
    -p 8080:8080 \
    -p 8081:8081 \
    --name bytecoin-fullnode \
    rafalsladek/bytecoin-docker

sudo trace-cmd record -e syscalls &
TRACE_CMD_PID=$!

sleep 600
sudo kill -SIGINT $TRACE_CMD_PID

docker-compose down
docker rm -f bytecoin-fullnode

sudo trace-cmd report > trace.txt
echo "완료되었습니다. 시스템 콜 데이터는 trace.txt 에 저장되었습니다."
