# ToDo: start with lighter base image. Started with conda because detectron2 is not detected without conda install
FROM continuumio/miniconda3

# install pip, gcc, g++ (needed for detectron2), git
RUN apt-get update && apt-get install -y python3-pip && apt-get install build-essential -y && apt-get install manpages-dev -y && apt-get -y install git

WORKDIR /textassistant

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY install.sh .
RUN chmod +x install.sh
RUN apt-get install gcc
# install requirements needed for detectron2
RUN ./install.sh
# needed for some image processing libraries used in detectron2
RUN apt-get install ffmpeg libsm6 libxext6  -y
# needed for getting YT audio from video
RUN pip install pytube==12.1.3
# needed for pandasai
RUN pip install pandasai==0.2.2
# needed for plotting graphs
RUN pip install seaborn==0.12.2

COPY Makefile .
COPY app.py app.py
COPY Home.py Home.py
COPY pages pages
# needed to change style of streamlit frontend
COPY style style
# needed to add Google Analytics
COPY index.html /opt/conda/lib/python3.10/site-packages/streamlit/static/index.html
# this is YT authentication token. Needed for downloading audio/video from YT
COPY tokens.json /opt/conda/lib/python3.10/site-packages/pytube/__cache__/tokens.json

ENV OPENAI_API_KEY=""
ENV ACTIVELOOP_TOKEN=""

COPY utils utils
# http needs port 80. https needs port 443
EXPOSE 8501
CMD ["make", "start_servers", "-j2"]
# use the following command instead of the above, for starting servers locally and testing.
# CMD ["make", "start_servers_locally", "-j2"]