FROM python:2.7.10
COPY requirements.txt /src/
RUN cd /src && pip install ipython && pip install -r requirements.txt
COPY . /src
WORKDIR /src/collector
