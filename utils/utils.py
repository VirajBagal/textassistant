################################################################################
# File: utils.py                                                               #
# Project: Spindle                                                             #
# Created Date: Friday, 28th April 2023 8:24:42 pm                             #
# Author: Viraj Bagal (viraj.bagal@synapsica.com)                              #
# -----                                                                        #
# Last Modified: Saturday, 29th April 2023 2:56:59 pm                          #
# Modified By: Viraj Bagal (viraj.bagal@synapsica.com)                         #
# -----                                                                        #
# Copyright (c) 2023 Synapsica                                                 #
################################################################################
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import YoutubeLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import DeepLake

LONG_VIDEO_THRESHOLD = 3500
REJECT_TOKENS_THRESHOLD = 100
YOUTUBE_URL = "https://www.youtube.com/watch?v=LbT1yp6quS8&ab_channel=PatrickLoeber"


def load_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    pages = loader.load_and_split()
    return pages


def form_embeddings(content, file_name):
    embeddings = OpenAIEmbeddings()
    db = DeepLake.from_documents(content, dataset_path=f"./database/{file_name}/", embedding=embeddings)
    return db


def load_youtube_url(url):
    loader = YoutubeLoader.from_youtube_url(url, add_video_info=False)
    result = loader.load()
    return result


def estimate_tokens(document):
    # taken from: https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them
    return int(len(document.page_content.split()) * 4 / 3)
