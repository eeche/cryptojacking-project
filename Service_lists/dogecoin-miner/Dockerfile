FROM ubuntu:22.04

RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get update
RUN apt-get install -y \
   wget \
   htop \
   tar \
   rsyslog

RUN wget -O /opt/pooler-cpuminer-linux-x86_64.tar.gz https://github.com/pooler/cpuminer/releases/download/v2.5.1/pooler-cpuminer-2.5.1-linux-x86_64.tar.gz
RUN tar xfz /opt/pooler-cpuminer-linux-x86_64.tar.gz -C /opt/

CMD ["/bin/bash","-c","echo '\n\n ***   USE AT YOUR OWN RISK    ***\n\n' && /opt/minerd --url=$URL --user=$USERNAME --pass=$PASSWORD --debug --protocol-dump"]
