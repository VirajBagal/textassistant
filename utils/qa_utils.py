################################################################################
# File: qa_utils.py                                                            #
# Project: Spindle                                                             #
# Created Date: Friday, 28th April 2023 8:27:55 pm                             #
# Author: Viraj Bagal (viraj.bagal@synapsica.com)                              #
# -----                                                                        #
# Last Modified: Friday, 5th May 2023 3:43:12 pm                               #
# Modified By: Viraj Bagal (viraj.bagal@synapsica.com)                         #
# -----                                                                        #
# Copyright (c) 2023 Synapsica                                                 #
################################################################################
from utils import utils
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
import logging
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI

logger = logging.getLogger("root")


def initialize_retriever(database):
    qa = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model="gpt-3.5-turbo"),
        chain_type="map_reduce",
        retriever=database.as_retriever(),
    )
    return qa


def prepare_files_for_qa(file_path):
    logger.info("Loading file for qa")
    content = []
    try:
        if ".pdf" in file_path:
            content = utils.load_pdf(file_path)
        elif ".doc" in file_path or ".docx" in file_path:
            content = utils.load_doc(file_path)
        elif ".png" in file_path or ".jpg" in file_path:
            content = utils.load_image(file_path)
        elif "csv" in file_path:
            content = utils.load_csv(file_path)
            logger.info("Dataframe loaded")
            llm = OpenAI()
            pandas_ai = PandasAI(llm)
            return pandas_ai, content

        logger.info("file loaded for qa")
        logger.info(f"Total number of pages are {len(content)}")
        total_tokens = utils.estimate_tokens(content)
        logger.info(f"Estimated tokens are {total_tokens}")
        # if total_tokens > utils.REJECT_TOKENS_THRESHOLD:
        #     logger.info(f"Rejecting request due to large number of tokens: {total_tokens}")
        #     return "Sorry! Too long"
        content = utils.split_text(content, chunk_size=3000, overlap=0)
        file_name = file_path.split("/")[-1].split(".")[0]
        logger.info("Creating embeddings")
        database = utils.form_embeddings(content, file_name)
        logger.info("Embeddings created. Now initializing retriever")
        retriever = initialize_retriever(database)
        logger.info("Retriever initialized")
    except:
        logging.exception("")
        return "File cannot be processed"
    return retriever, content


def prepare_yt_video_for_qa(yt_url):
    try:
        logger.info("Loading YT content")
        content = utils.load_youtube_url(yt_url)
        logger.info("YT content loaded")
        num_tokens = utils.estimate_tokens(content)
        logger.info(f"Estimated tokens are {num_tokens}")
        # if num_tokens > utils.REJECT_TOKENS_THRESHOLD:
        #     logger.info(f"Rejecting request due to large number of tokens: {num_tokens}")
        #     return "Sorry! Too long"
        content = utils.split_text(content, chunk_size=3000, overlap=0)
        video_uid = yt_url.split("watch?")[-1].split(" ")[-1]
        logger.info("Creating embeddings")
        database = utils.form_embeddings(content, video_uid)
        logger.info("Embeddings created. Now initializing retriever")
        retriever = initialize_retriever(database)
        logger.info("Retriever initialized")
    except:
        logging.exception("")
        return "Video cannot be processed"
    return retriever, content
