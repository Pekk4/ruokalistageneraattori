FROM python:3.9-slim

WORKDIR /app

COPY ./requirements.txt .

RUN pip3 install -r requirements.txt
RUN mkdir logs
RUN useradd user && chown -R user /app

COPY . .

WORKDIR /app/src/

USER user

CMD [ "gunicorn", "-b", "0.0.0.0:8000", "app:app" ]
