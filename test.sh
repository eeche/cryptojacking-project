#!/bin/bash

SAVE_DIR=/media/eeche/0E2A-EE70/syscall
mkdir -p $SAVE_DIR

sudo trace-cmd record -e syscalls &
TRACE_CMD_PID=$!
sleep 10
sudo kill -SIGINT $TRACE_CMD_PID
sleep 5

DOGECOIN_MINER_DIR="./Service_lists/dogecoin-miner"
(cd $DOGECOIN_MINER_DIR && docker-compose up --build -d)

sleep 30
sudo trace-cmd record -e syscalls &
TRACE_CMD_PID=$!

sleep 600

sudo kill -SIGINT $TRACE_CMD_PID
sleep 30

sudo trace-cmd report > $SAVE_DIR/test_doge.txt
echo "시스템 콜 데이터는 $SAVE_DIR/test_doge.txt 에 저장되었습니다."
sleep 10

(cd $DOGECOIN_MINER_DIR && docker-compose down)
