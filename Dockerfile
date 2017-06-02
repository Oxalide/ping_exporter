FROM python:3.6

WORKDIR /exporter
ADD requirements.txt ./
RUN pip install -r requirements.txt

ADD exporter.py ./

CMD python exporter.py --target www.oxalide.com --icmp --tcp 80 443
