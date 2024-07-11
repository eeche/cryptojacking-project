#!/bin/bash
NUM_ITERATIONS=5

docker-compose up -d

docker run -d --name locust_temp \
  -v $(pwd)/locustfile.py:/mnt/locust/locustfile.py \
  locustio/locust \
  -f /mnt/locust/locustfile.py --headless -u 100 -r 10 --host http://nginx

sleep 100

SAVE_DIR=/media/eeche/0E2A-EE70/syscall
mkdir -p $SAVE_DIR

sudo trace-cmd record -e syscalls &
TRACE_CMD_PID=$!
sleep 10
sudo kill -SIGINT $TRACE_CMD_PID
sleep 5

for ((n=1; n<=25; n++))
do
    sudo trace-cmd record -e syscalls &
    TRACE_CMD_PID=$!

    sleep 600

    sudo kill -SIGINT $TRACE_CMD_PID
    sleep 30

    sudo trace-cmd report > $SAVE_DIR/data_analyze_$n.txt
    echo "시스템 콜 데이터는 $SAVE_DIR/data_analyze_$n.txt 에 저장되었습니다."
    sleep 10
done

docker run -d \
    -e TZ=Europe/Berlin \
    -v /root/bytecoin \
    --restart unless-stopped \
    -p 8082:8082 \
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

    sudo trace-cmd report > $SAVE_DIR/data_analyze_bytecoin_$n.txt
    echo "시스템 콜 데이터는 $SAVE_DIR/data_analyze_bytecoin_$n.txt 에 저장되었습니다."
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
    
    sudo trace-cmd report > $SAVE_DIR/data_analyze_dashcoin_$n.txt
    echo "시스템 콜 데이터는 $SAVE_DIR/data_analyze_dashcoin_$n.txt 에 저장되었습니다."
    sleep 10
done

docker rm -f dash-livenet
docker run -d --name doge-xmrig eeche/doge-xmrig

for ((n=1; n<=NUM_ITERATIONS; n++))
do
    sudo trace-cmd record -e syscalls &
    TRACE_CMD_PID=$!

    sleep 600

    sudo kill -SIGINT $TRACE_CMD_PID
    sleep 30
    
    sudo trace-cmd report > $SAVE_DIR/data_analyze_doge_$n.txt
    echo "시스템 콜 데이터는 $SAVE_DIR/data_analyze_doge_$n.txt 에 저장되었습니다."
    sleep 10
done

docker rm -f doge-xmrig
docker run --name monero-miner \
    --network host \
    -d giansalex/monero-miner \
    /xmr/xmrig -o pool.supportxmr.com:3333 \
    -u 43mquVNuaUaiz7akGc1C4bbZbws6tJtHJN3DK66SCSj9igF4Ndbebs6Q98Ao9vFPiyhqWd8WHfBAfTarYQjGpqCs8PNLwcg \
    -k --cpu-priority=2

for ((n=1; n<=NUM_ITERATIONS; n++))
do
    sudo trace-cmd record -e syscalls &
    TRACE_CMD_PID=$!

    sleep 600

    sudo kill -SIGINT $TRACE_CMD_PID
    sleep 30
    
    sudo trace-cmd report > $SAVE_DIR/data_analyze_monero_$n.txt
    echo "시스템 콜 데이터는 $SAVE_DIR/data_analyze_monero_$n.txt 에 저장되었습니다."
    sleep 10
done

docker rm -f monero-miner
docker run -d --name nimiq-miner \
    --network host eeche/nimiq-miner:latest \
    /usr/share/nimiq/app/node /usr/share/nimiq/app/index.js \
    --miner=2 --pool=pool.acemining.co:8443 \
    --type=light \
    --wallet-address=NQ6272GHCS6H3XL5L09SFGAM34MK7CU11JFE \
    --protocol=ws \
    --host=pool.acemining.co \
    --port=8443

for ((n=1; n<=NUM_ITERATIONS; n++))
do
    sudo trace-cmd record -e syscalls &
    TRACE_CMD_PID=$!

    sleep 600

    sudo kill -SIGINT $TRACE_CMD_PID
    sleep 30
    
    sudo trace-cmd report > $SAVE_DIR/data_analyze_nimiq_$n.txt
    echo "시스템 콜 데이터는 $SAVE_DIR/data_analyze_nimiq_$n.txt 에 저장되었습니다."
    sleep 10
done

sudo aa-remove-unknown
docker-compose down
docker rm -f locust_temp
docker rm -f miniq-miner
