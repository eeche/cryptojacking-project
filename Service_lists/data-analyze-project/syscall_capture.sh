#!/bin/bash
NUM_ITERATIONS=5

docker-compose up -d

docker run -d --name locust_temp \
  -v $(pwd)/locustfile.py:/mnt/locust/locustfile.py \
  locustio/locust \
  -f /mnt/locust/locustfile.py --headless -u 100 -r 10 --host http://nginx

sleep 100

SAVE_DIR=~/Desktop/syscall
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
    sleep 5

    sudo trace-cmd report > $SAVE_DIR/data_analyze_$n.txt
    echo "시스템 콜 데이터는 $SAVE_DIR/data_analyze_$n.txt 에 저장되었습니다."
    sleep 10
done

docker run -d \
    -e TZ=Europe/Berlin \
    -v ~/.bytecoin:/root/.bytecoin \
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
    sleep 5

    sudo trace-cmd report > $SAVE_DIR/data_analyze_bytecoin_$n.txt
    echo "시스템 콜 데이터는 $SAVE_DIR/data_analyze_bytecoin_$n.txt 에 저장되었습니다."
    sleep 10
done

sudo aa-remove-unknown
docker-compose down
docker rm -f bytecoin-fullnode
docker rm -f locust_temp