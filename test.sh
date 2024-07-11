#!/bin/bash

SAVE_DIR=/media/eeche/0E2A-EE70/syscall
mkdir -p $SAVE_DIR

sudo trace-cmd record -e syscalls &
TRACE_CMD_PID=$!
sleep 10
sudo kill -SIGINT $TRACE_CMD_PID
sleep 5

# DOGECOIN_MINER_DIR="./Service_lists/dogecoin-miner"
# (cd $DOGECOIN_MINER_DIR && docker-compose up --build -d)

# sleep 30
# sudo trace-cmd record -e syscalls &
# TRACE_CMD_PID=$!

# sleep 600

# sudo kill -SIGINT $TRACE_CMD_PID
# sleep 30

# sudo trace-cmd report > $SAVE_DIR/doge.txt
# echo "시스템 콜 데이터는 $SAVE_DIR/doge.txt 에 저장되었습니다."
# sleep 10

# (cd $DOGECOIN_MINER_DIR && docker-compose down)

# docker run --name monero-miner --network host -d giansalex/monero-miner /xmr/xmrig -o pool.supportxmr.com:3333 -u 43mquVNuaUaiz7akGc1C4bbZbws6tJtHJN3DK66SCSj9igF4Ndbebs6Q98Ao9vFPiyhqWd8WHfBAfTarYQjGpqCs8PNLwcg -k --cpu-priority=2

# sleep 30
# sudo trace-cmd record -e syscalls &
# TRACE_CMD_PID=$!

# sleep 600

# sudo kill -SIGINT $TRACE_CMD_PID
# sleep 30

# sudo trace-cmd report > $SAVE_DIR/monero.txt
# echo "시스템 콜 데이터는 $SAVE_DIR/monero.txt 에 저장되었습니다."
# sleep 10

# docker rm -f monero-miner

docker run -d --name doge-xmrig eeche/doge-xmrig

sleep 30
sudo trace-cmd record -e syscalls &
TRACE_CMD_PID=$!

sleep 600

sudo kill -SIGINT $TRACE_CMD_PID
sleep 30

sudo trace-cmd report > $SAVE_DIR/doge.txt
echo "시스템 콜 데이터는 $SAVE_DIR/doge.txt 에 저장되었습니다."
sleep 10

docker rm -f doge-xmrig

