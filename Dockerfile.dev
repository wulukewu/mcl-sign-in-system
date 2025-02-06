# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt

# Install Chrome and Xvfb
RUN apt-get update && apt-get install -y wget gnupg
RUN wget -qO - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN apt-get update && apt-get install -y google-chrome-stable xvfb

# Install additional dependencies for ChromeDriver
RUN apt-get install -y fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 libatk1.0-0 libcups2 libdbus-1-3 libdrm2 libgbm1 libnspr4 libnss3 libxcomposite1 libxrandr2 xdg-utils

# Install ffmpeg
RUN apt-get install -y ffmpeg

# Set environment variables
ENV DISPLAY=:99

# Command to run the application
ENTRYPOINT ["python", "main.py"]