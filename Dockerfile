FROM python:3.9-bookworm
RUN apt-get update \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
COPY . /app/
WORKDIR /app/
RUN pip3 install --no-cache-dir -U pip
RUN pip3 install --no-cache-dir -U -r requirements.txt
CMD bash start
