FROM python:3.12

WORKDIR /

RUN pip install aiogram

RUN pip install python-dotenv

ADD ./app /app

ADD ./app/start.py /

CMD ["python", "start.py"]