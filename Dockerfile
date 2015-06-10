FROM centos:centos6

RUN yum install -y gcc python python-pip python-devel openssl-devel sqlite sqlite-devel libxslt-devel libxml2-devel zlib-devel libffi-devel wget bc which tar

RUN useradd synda

ENV ST_HOME=/home/synda/sdt
ENV PATH=$ST_HOME/bin:$PATH

RUN su synda -c " mkdir -p /home/synda/src/synda && cd /home/synda/src/synda && wget https://raw.githubusercontent.com/Prodiguer/synda/master/sdc/install.sh && chmod +x install.sh && ./install.sh"

RUN wget -O /tmp/boot.sh http://esgf-build.ipsl.upmc.fr/boot.sh; cat /tmp/boot.sh >> /root/.bashrc

RUN su synda -c "wget -O /tmp/env.sh http://esgf-build.ipsl.upmc.fr/env.sh; cat /tmp/env.sh >> /home/synda/.bashrc"


