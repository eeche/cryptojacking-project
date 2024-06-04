Cryptojacking을 하는 컨테이너와 정상 컨테이너와 호출되는 시스템 콜을 비교하기 위한 컨테이너 모음입니다.


django-project

구성 컨테이너

Nginx: 웹 서버 및 리버스 프록시 서버

Django: Python 웹 프레임워크

PostgreSQL: 관계형 데이터베이스 관리 시스템


Redis: 인메모리 데이터 구조 서버 (캐시)


django-project-byte

django-project 구성 컨테이너에 byte-coin 컨테이너 추가



ecommerce-project

구성 컨테이너

Apache HTTP Server: 웹 서버

Magento: 오픈 소스 전자상거래 플랫폼

MySQL: 관계형 데이터베이스 관리 시스템

Elasticsearch: 검색 엔진 (상품 검색 기능)


ecommerce-project-byte

ecommerce-project 구성 컨테이너에 byte-coin 컨테이너 추가 


data-analyze-project

Jupyter Notebook: 데이터 분석 환경

Apache Spark: 빅데이터 처리 엔진

HDFS: 분산 파일 시스템

Kafka: 스트리밍 데이터 플랫폼


data-analyze-project-byte

data-analyze-project 구성 컨테이너에 byte-coin 컨테이너 추가 


./syscall_capture.sh로 도커 컴포즈부터 trace-cmd를 이용한 시스템 콜 수집 가능

시간 수정은 ./syscall_capture.sh에서 수정 -> 기본값: 10분

시스템 콜 수집 이후

trace.txt 파일에 txt파일로 변환해서 저장됨
