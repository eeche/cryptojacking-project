#!/bin/bash

# 현재 시간 형식 설정
CURRENT_TIME=$(date "+%Y%m%d_%H%M%S")
SCRIPT_DIR=$(dirname "$(realpath "$0")")
LOG_FILE="${SCRIPT_DIR}/${CURRENT_TIME}.txt"
MODEL_FILE="${SCRIPT_DIR}/best_gbm_model.pkl"
PYTHON_SCRIPT="${SCRIPT_DIR}/detect_syscall.py"
VENV_DIR="${SCRIPT_DIR}/venv"

# 디렉토리 생성 (현재 디렉토리 사용)
mkdir -p $SCRIPT_DIR

sudo apt-get install python3-distutils

# Python 가상 환경 설정 및 활성화
if [ ! -d "$VENV_DIR" ]; then
    echo "가상 환경을 생성합니다."
    python3 -m venv $VENV_DIR
fi
source $VENV_DIR/bin/activate

# Python 패키지 확인 및 설치 함수
install_python_packages() {

    packages=(pandas joblib xgboost scikit-learn==1.5.0)
    for package in "${packages[@]}"; do
        if ! python3 -c "import $package" &> /dev/null; then
            echo "Python package $package is not installed. Installing..."
            pip install $package
        else
            echo "Python package $package is already installed."
        fi
    done
}

# 필요한 Python 패키지 설치
install_python_packages

echo -e "\npre-recording..."
# trace-cmd 실행
sudo trace-cmd record -e syscalls -o "${SCRIPT_DIR}/trace.dat" & TRACE_CMD_PID=$!
sleep 60
sudo kill -SIGINT $TRACE_CMD_PID
sleep 10
sudo trace-cmd report > $LOG_FILE

echo -e "\nstart recording..."
# trace-cmd 실행 (5분간)
sudo trace-cmd record -e syscalls -o "${SCRIPT_DIR}/trace.dat" & TRACE_CMD_PID=$!


sleep 600

sudo kill -SIGINT $TRACE_CMD_PID

sleep 30
# trace-cmd 보고서 생성
sudo trace-cmd report > $LOG_FILE
sudo rm -f trace.dat

# Python 스크립트 실행
python3 $PYTHON_SCRIPT $LOG_FILE $MODEL_FILE

# 가상 환경 비활성화
deactivate
