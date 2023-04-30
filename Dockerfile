FROM continuumio/anaconda3

RUN apt-get update && apt-get install -y python3-pip && apt-get install build-essential -y && apt-get install manpages-dev -y && apt-get -y install git

WORKDIR /textassistant

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY install.sh .
RUN chmod +x install.sh
RUN apt-get install gcc
RUN ./install.sh

RUN apt-get install ffmpeg libsm6 libxext6  -y
# RUN python -m nltk.downloader -d /root/nltk_data punkt
# RUN python -m nltk.downloader -d /root/nltk_data averaged_perceptron_tagger

COPY Makefile .
COPY app.py app.py
COPY frontend.py frontend.py

ENV OPENAI_API_KEY="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"
ENV ACTIVELOOP_TOKEN="eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4MjUxMTQ0MCwiZXhwIjoxNjkzNDg0MTU5fQ.eyJpZCI6InZpcmFqYmFnYWwxMiJ9.wo5zcCGse8v1d2SRXx_4ZjPW0Lo-SRIFCJvrmRyQyHq8nay40KumNhlXaexDY8ylOegBsCNzZDdr7ADbaSsSDA"

COPY utils utils
EXPOSE 8501
CMD ["make", "start_servers", "-j2"]