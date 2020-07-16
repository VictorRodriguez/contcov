FROM ubuntu

RUN apt-get update
RUN apt install -y docker.io
RUN apt-get -y install curl python3 python3-pip
RUN pip3 install jinja2
RUN curl -LO https://storage.googleapis.com/container-diff/latest/container-diff-linux-amd64 && chmod +x container-diff-linux-amd64
RUN mkdir -p $HOME/bin
RUN mv container-diff-linux-amd64 $HOME/bin/container-diff
COPY run.sh .
COPY html_report.py .
COPY components .
COPY template.html .
COPY clear_analyzer.py .
RUN mkdir -p /opt/result
CMD bash run.sh && cp *.html /opt/result
