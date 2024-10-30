FROM python:3.9

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y wget unzip \
    && wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/`curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
    && rm /tmp/chromedriver.zip

CMD ["python", "main.py"]