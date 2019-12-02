FROM python:3.7.1

ENV PYTHONDONTWRITEBYTECODE 1
ENV FLASK_APP "./namenode.py"
ENV FLASK_ENV "development"
ENV FLASK_DEBUG True

RUN mkdir /app
WORKDIR /app

ADD . /app
ADD ./requirements.txt ./app/requirements.txt
RUN pip install -r requirements.txt

ADD namenode.py /app

EXPOSE 5000

CMD flask run --host=0.0.0.0