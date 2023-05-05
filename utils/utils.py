################################################################################
# File: utils.py                                                               #
# Project: Spindle                                                             #
# Created Date: Friday, 28th April 2023 8:24:42 pm                             #
# Author: Viraj Bagal (viraj.bagal@synapsica.com)                              #
# -----                                                                        #
# Last Modified: Saturday, 6th May 2023 1:46:18 am                             #
# Modified By: Viraj Bagal (viraj.bagal@synapsica.com)                         #
# -----                                                                        #
# Copyright (c) 2023 Synapsica                                                 #
################################################################################
from langchain.docstore.document import Document
from langchain.document_loaders import PyPDFLoader, UnstructuredWordDocumentLoader, YoutubeLoader
from langchain.document_loaders.image import UnstructuredImageLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import DeepLake
from langchain.text_splitter import RecursiveCharacterTextSplitter
import logging
import openai
import os
from pytube import YouTube
import pandas as pd

logger = logging.getLogger("root")

LONG_VIDEO_THRESHOLD = 3500
REJECT_TOKENS_THRESHOLD = 10000
YOUTUBE_URL = "https://www.youtube.com/watch?v=LbT1yp6quS8&ab_channel=PatrickLoeber"


def load_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    pages = loader.load_and_split()
    return pages


def load_doc(doc_path):
    loader = UnstructuredWordDocumentLoader(doc_path)
    data = loader.load()
    return data


def load_image(image_path):
    loader = UnstructuredImageLoader(image_path)
    data = loader.load()
    return data


def load_csv(csv_path):
    if "csv" in csv_path:
        return pd.read_csv(csv_path)
    return pd.read_excel(csv_path)


def split_text(document, chunk_size, overlap):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    texts = text_splitter.split_documents(document)
    return texts


def form_embeddings(content, file_name):
    embeddings = OpenAIEmbeddings()
    db = DeepLake.from_documents(content, dataset_path=f"./database/{file_name}/", embedding=embeddings)
    return db


def convert_from_mobile_url(url):
    # convert mobile yt url
    # https://m.youtube.com/watch?v=LDVyOnf0t9M&feature=youtu.be  ---> https://m.youtube.com/watch?v=LDVyOnf0t9M
    url = url.replace("&feature=youtu.be", "")
    # https://m.youtube.com/watch?v=LDVyOnf0t9M ---> https://www.youtube.com/watch?v=LDVyOnf0t9M
    url = url.replace("m.youtube", "www.youtube")
    # https://youtu.be/LDVyOnf0t9M ---> https://www.youtube.com/watch?v=LDVyOnf0t9M
    url = url.replace("youtu.be/", "www.youtube.com/watch?v=")
    return url


def audio_download_path(url):
    video_id = url.split("watch?v=")[-1]
    return os.path.join("./received_files/", video_id + ".mp4")


def download_youtube_audio(url):
    try:
        video = YouTube(url, use_oauth=True, allow_oauth_cache=True)
        # filtering the audio. File extension can be mp4/webm
        # You can see all the available streams by print(video.streams)
        video_id = url.split("watch?v=")[-1]
        logger.info(f"Getting streams of video with id {video_id}")
        logger.info(f"Available streams are: \n {video.streams}")
        audio = video.streams.filter(only_audio=True, file_extension="mp4").first()
        audio.download(output_path="./received_files/", filename=video_id + ".mp4")
        logger.info("Download Completed!")
        return True
    except:
        logger.error("Connection Error")  # to handle exception
        return False


def save_transcript(content, path):
    with open(path.replace("mp4", "txt"), "w") as f:
        f.write(content)


def read_transcript(path):
    return open(path, "r").read()


def load_youtube_url(url):
    url = convert_from_mobile_url(url)
    loader = YoutubeLoader.from_youtube_url(url, add_video_info=False)
    # ToDo: upgrade langchain version in docker to take care of this
    try:
        result = loader.load()
    except:
        result = []
    # if captions are not available, result will be empty. So run speech-to-text model
    if not result:
        audio_path = audio_download_path(url)
        # check if transcription is already available
        is_transcription_available = os.path.exists(audio_path.replace("mp4", "txt"))
        # check if audio is already downloaded or transcription is already available. If not, then download the audio
        is_audio_downloaded = (
            True if (os.path.exists(audio_path) or is_transcription_available) else download_youtube_audio(url)
        )
        # if audio is available (either already present or downloaded), and transcription is not available, then trigger Whisper model and save the transcript
        if is_audio_downloaded and not is_transcription_available:
            logger.info(
                f"Transcription/translation not found at {audio_path.replace('mp4', 'txt')}. So triggered Whisper model"
            )
            audio_file = open(audio_path, "rb")
            # send file to Whisper API. Translate is used because ChatGPT summarization was not good for other languages than English.
            transcript = openai.Audio.translate("whisper-1", audio_file)
            save_transcript(transcript["text"], audio_path)
            logger.info(f"Transcription/translation saved at {audio_path.replace('mp4', 'txt')}")
            result = [Document(page_content=transcript["text"])]
        # if transcription is available, then read the transcript
        elif is_transcription_available:
            logger.info(f"Transcription already present at {audio_path.replace('mp4', 'txt')}. So using it.")
            text = read_transcript(audio_path.replace("mp4", "txt"))
            result = [Document(page_content=text)]
        if os.path.exists(audio_path):
            # delete the downloaded audio since the transcript is saved
            os.remove(audio_path)
    return result


def estimate_tokens(document):
    # taken from: https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them
    total_tokens = 0
    for doc in document:
        total_tokens += int(len(doc.page_content.split()) * 4 / 3)
    return total_tokens
