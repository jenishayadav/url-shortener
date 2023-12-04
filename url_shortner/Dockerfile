FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get upgrade -y && apt-get autoremove -y

COPY ./requirements.txt ./

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install -r requirements.txt

COPY ./ ./

EXPOSE 5000

CMD ["python3", "run.py"]
