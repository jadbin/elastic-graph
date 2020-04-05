FROM python:3.6

ADD ./ /opt/elastic_graph
WORKDIR /opt/elastic_graph

RUN chmod +x bin/manage \
  && pip install -r requirements/app.txt

CMD bin/manage start --daemon-off
