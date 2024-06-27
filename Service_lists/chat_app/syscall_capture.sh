#!/bin/bash
NUM_ITERATIONS=5

docker-compose up -d

docker run -d --name locust_chat \
  -v $(pwd)/locustfile.py:/mnt/locust/locustfile.py \
  locustio/locust \
  -f /mnt/locust/locustfile.py --headless -u 100 -r 10 --host http://node:3000

sleep 100

SAVE_DIR=/media/eeche/0E2A-EE70/syscall
mkdir -p $SAVE_DIR

sudo trace-cmd record -e syscalls &
TRACE_CMD_PID=$!
sleep 10
sudo kill -SIGINT $TRACE_CMD_PID
sleep 5

for ((n=1; n<=NUM_ITERATIONS; n++))
do
    sudo trace-cmd record -e syscalls &
    TRACE_CMD_PID=$!

    sleep 600

    sudo kill -SIGINT $TRACE_CMD_PID
    sleep 30
    
    sudo trace-cmd report > $SAVE_DIR/chat_$n.txt
    echo "시스템 콜 데이터는 $SAVE_DIR/chat_$n.txt 에 저장되었습니다."

    sleep 10
done

docker run -d \
    -e TZ=Europe/Berlin \
    -v /root/bytecoin \
    --restart unless-stopped \
    -p 8080:8080 \
    -p 8081:8081 \
    --name bytecoin-fullnode \
    rafalsladek/bytecoin-docker

sleep 10

for ((n=1; n<=NUM_ITERATIONS; n++))
do
    sudo trace-cmd record -e syscalls &
    TRACE_CMD_PID=$!

    sleep 600

    sudo kill -SIGINT $TRACE_CMD_PID
    sleep 30
    
    sudo trace-cmd report > $SAVE_DIR/chat_bytecoin_$n.txt
    echo "시스템 콜 데이터는 $SAVE_DIR/chat_bytecoin_$n.txt 에 저장되었습니다."

    sleep 10
done

docker rm -f bytecoin-fullnode
docker run -e DASH_LIVENET=1 -d -p 3001:3001 -p 9999:9999 -v /root/dash-node/livenet --name dash-livenet berrywallet/bitcore-node-dash

for ((n=1; n<=NUM_ITERATIONS; n++))
do
    sudo trace-cmd record -e syscalls &
    TRACE_CMD_PID=$!

    sleep 600

    sudo kill -SIGINT $TRACE_CMD_PID
    sleep 30
    
    sudo trace-cmd report > $SAVE_DIR/chat_bitcore_$n.txt
    echo "시스템 콜 데이터는 $SAVE_DIR/chat_bitcore_$n.txt 에 저장되었습니다."
    sleep 10
done

sudo aa-remove-unknown
docker-compose down
docker rm -f locust_chat
docker rm -f dash-livenet