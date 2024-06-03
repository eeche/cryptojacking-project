djangoProject 웹서버에서 파일 locust 이용해서 /, /about, /contact 를 접속하면서 트래픽 생성하는 컨테이너

./syscall_capture.sh로 도커 컴포즈부터 trace-cmd를 이용한 시스템 콜 수집 가능

시간 수정은 ./syscall_capture.sh에서 수정 -> 테스트를 위해 10초로 되어있음

시스템 콜 수집 이후

trace-cmd report -i trace.dat > trace.txt

로 txt파일로 변환해서 사용
