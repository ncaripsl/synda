FROM centos:centos6

RUN yum install -y gcc python python-pip python-devel openssl-devel sqlite sqlite-devel libxslt-devel libxml2-devel zlib-devel libffi-devel wget bc which tar

RUN useradd synda

RUN su synda -c "echo 'ST_HOME=/home/synda/sdt' >> /home/synda/.bashrc; echo 'PATH=$ST_HOME/bin:$PATH' >> /home/synda/.bashrc"

RUN su synda -c "mkdir -p /home/synda/src/synda && cd /home/synda/src/synda && wget https://raw.githubusercontent.com/Prodiguer/synda/master/sdc/install.sh && chmod +x install.sh && ./install.sh"

RUN wget -O /tmp/synda_autologin.sh http://esgf-build.ipsl.upmc.fr/synda_autologin.sh; cat /tmp/synda_autologin.sh >> /root/.bashrc




