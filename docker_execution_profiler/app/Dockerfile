FROM ubuntu:16.04

RUN apt-get -yqq update

RUN apt-get -yqq install python3-pip python3-dev libssl-dev libffi-dev

RUN apt-get install -y openssh-server

ADD requirements.txt /requirements.txt

RUN pip3 install -r requirements.txt

ADD dag.txt /dag.txt

ADD local_pro.py /local_pro.py
ADD aggregate0.py /aggregate0.py
ADD aggregate1.py /aggregate1.py
ADD aggregate2.py /aggregate2.py
ADD simple_detector0.py /simple_detector0.py
ADD simple_detector1.py /simple_detector1.py
ADD simple_detector2.py /simple_detector2.py
ADD astute_detector0.py /astute_detector0.py
ADD astute_detector1.py /astute_detector1.py
ADD astute_detector2.py /astute_detector2.py 
ADD fusion_center0.py /fusion_center0.py 
ADD fusion_center1.py /fusion_center1.py 
ADD fusion_center2.py /fusion_center2.py 
ADD global_fusion.py /global_fusion.py 
ADD admd.py /admd.py

ADD 1botnet.ipsum /1botnet.ipsum

ADD profiler.py /profiler.py

ADD start.sh /start.sh

WORKDIR /

EXPOSE 22

CMD ["./start.sh"]
