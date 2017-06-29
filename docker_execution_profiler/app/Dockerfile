FROM ubuntu:16.04

RUN apt-get -yqq update

RUN apt-get -yqq install python3-pip python3-dev libssl-dev libffi-dev

RUN apt-get install -y openssh-server

ADD requirements.txt /requirements.txt

RUN pip3 install -r requirements.txt

ADD dag.txt /dag.txt

ADD task1.py /task1.py

ADD task2.py /task2.py

ADD task3.py /task3.py

ADD task4.py /task4.py

ADD input.txt /input.txt

ADD profiler.py /profiler.py

ADD start.sh /start.sh

WORKDIR /

EXPOSE 22

CMD ["./start.sh"]
