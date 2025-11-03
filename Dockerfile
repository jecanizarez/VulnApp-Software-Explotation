FROM python:3.10
COPY . /
ENV PYTHONPATH=${PYTHONPATH}:${PWD}
RUN pip3 install -r requirements.txt
