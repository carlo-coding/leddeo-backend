FROM python:3.8-slim-buster
ADD . /
RUN apt-get update \
  && apt-get install -y wget \
  && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y git
RUN pip install -r requirements.txt
RUN apt install ffmpeg -y
RUN apt install imagemagick -y 
RUN sed -i '88d' ~/../etc/ImageMagick-6/policy.xml 
RUN chmod +x run.sh
WORKDIR /

CMD [ "./run.sh" ]