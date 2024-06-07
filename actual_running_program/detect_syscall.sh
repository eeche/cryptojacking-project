#!/bin/bash

# 현재 시간 형식 설정
CURRENT_TIME=$(date "+%Y%m%d_%H%M%S")
SCRIPT_DIR=$(dirname "$(realpath "$0")")
LOG_FILE="${SCRIPT_DIR}/${CURRENT_TIME}.txt"
FREQUENCY_FILE="${LOG_FILE%.txt}_frequency.txt"
MODEL_FILE="${SCRIPT_DIR}/voting_classifier_model.pkl"
SCALER_FILE="${SCRIPT_DIR}/scaler.pkl"
PYTHON_SCRIPT="${SCRIPT_DIR}/detect_syscall.py"
TRACE_CMD="/usr/bin/trace-cmd"  # trace-cmd의 절대 경로

# 디렉토리 생성 (현재 디렉토리 사용)
mkdir -p $SCRIPT_DIR

# trace-cmd 실행 (5분간)
sudo $TRACE_CMD record -e syscalls -o "${SCRIPT_DIR}/trace.dat" & TRACE_CMD_PID=$!

sleep 300

sudo kill -SIGINT $TRACE_CMD_PID

# trace-cmd 보고서 생성
sudo $TRACE_CMD report "${SCRIPT_DIR}/trace.dat" > $LOG_FILE

# Python 스크립트 실행
sudo -H python3 $PYTHON_SCRIPT $LOG_FILE $MODEL_FILE $SCALER_FILE $FREQUENCY_FILE
