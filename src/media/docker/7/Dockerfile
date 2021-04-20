FROM ubuntu

EXPOSE 8080

RUN sed -i 's/archive.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list && apt update && apt install -y netcat && apt clean

CMD while true;do nc -l -p 8080; echo "End of session\n"; done