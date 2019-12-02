FROM python:3.7.1

RUN mkdir /app
WORKDIR /app

ADD . /app
ADD ./requirements.txt ./app/requirements.txt
RUN pip install -r requirements.txt

ADD client.py /app
ADD new_key.pem /app

CMD python -u client.py