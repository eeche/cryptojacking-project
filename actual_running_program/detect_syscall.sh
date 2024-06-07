#!/bin/bash

# 현재 시간 형식 설정
CURRENT_TIME=$(date "+%Y%m%d_%H%M%S")
LOG_DIR="/tmp/cjcheck"
LOG_FILE="${LOG_DIR}/${CURRENT_TIME}.txt"
FREQUENCY_FILE="${LOG_FILE}_frequency.txt"
MODEL_FILE="random_forest_model.pkl"
SCALER_FILE="scaler.pkl"
PYTHON_SCRIPT="/detect_syscall.py"

# 디렉토리 생성
mkdir -p $LOG_DIR

# sudo 권한으로 trace-cmd 실행 (5분간)
sudo trace-cmd record -e syscall &
TRACE_CMD_PID=$!

sleep 300

sudo kill -SIGINT $TRACE_CMD_PID

# trace-cmd 보고서 생성
sudo trace-cmd report > $LOG_FILE

# Python 스크립트 실행
python3 $PYTHON_SCRIPT $LOG_FILE $MODEL_FILE $SCALER_FILE
