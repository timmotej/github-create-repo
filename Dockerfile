FROM python:slim

RUN apt-get update -y && apt-get  install -y vim
RUN pip install -U pip
RUN pip install -U requests click
COPY app /app
WORKDIR /app
CMD ["python", "main.py"]
