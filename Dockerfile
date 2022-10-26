FROM python:3.7.13
WORKDIR /src
RUN apt-get update -y && apt-get install -y --no-install-recommends build-essential gcc \libsndfile1 
RUN pip3 install --upgrade pip
RUN apt-get update && apt-get install ffmpeg -y
COPY ./requirements.txt /src/requirements.txt
RUN pip3 install -r requirements.txt
COPY . /src
EXPOSE 8112
CMD  ["python","main.py"]