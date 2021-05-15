FROM ubuntu
WORKDIR /home/ctf

RUN sed -i 's/archive.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list \
        && apt-get update
COPY buffer .
COPY flag .
COPY ynetd .
EXPOSE 1024
RUN chmod 0777 -R /home/ctf

CMD ./ynetd -p 1024 ./buffer
