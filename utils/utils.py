################################################################################
# File: utils.py                                                               #
# Project: Spindle                                                             #
# Created Date: Friday, 28th April 2023 8:24:42 pm                             #
# Author: Viraj Bagal (viraj.bagal@synapsica.com)                              #
# -----                                                                        #
# Last Modified: Wednesday, 3rd May 2023 6:34:05 pm                            #
# Modified By: Viraj Bagal (viraj.bagal@synapsica.com)                         #
# -----                                                                        #
# Copyright (c) 2023 Synapsica                                                 #
################################################################################
from langchain.document_loaders import PyPDFLoader, UnstructuredWordDocumentLoader, YoutubeLoader
from langchain.document_loaders.image import UnstructuredImageLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import DeepLake
from langchain.text_splitter import RecursiveCharacterTextSplitter

LONG_VIDEO_THRESHOLD = 3500
REJECT_TOKENS_THRESHOLD = 20000
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


def load_youtube_url(url):
    url = convert_from_mobile_url(url)
    loader = YoutubeLoader.from_youtube_url(url, add_video_info=False)
    result = loader.load()
    return result


def estimate_tokens(document):
    # taken from: https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them
    return int(len(document.page_content.split()) * 4 / 3)
