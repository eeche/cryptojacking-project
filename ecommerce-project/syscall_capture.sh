#!/bin/bash

docker-compose up -d locust

sudo trace-cmd record -e syscalls &
TRACE_CMD_PID=$!

sleep 600
sudo kill -SIGINT $TRACE_CMD_PID

docker-compose down
sudo trace-cmd report > trace.txt

echo "완료되었습니다. 시스템 콜 데이터는 trace.txt 에 저장되었습니다."
