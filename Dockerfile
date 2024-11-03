#
FROM python:3.9

#
WORKDIR /app

#
COPY . /app

#
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y wget gnupg
RUN wget -qO - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN apt-get update && apt-get install -y google-chrome-stable

#
ENTRYPOINT ["python", "main.py"]
# CMD ["python", "main.py"]
