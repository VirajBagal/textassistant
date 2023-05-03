################################################################################
# File: app.py                                                                 #
# Project: Spindle                                                             #
# Created Date: Thursday, 27th April 2023 5:27:15 pm                           #
# Author: Viraj Bagal (viraj.bagal@synapsica.com)                              #
# -----                                                                        #
# Last Modified: Tuesday, 2nd May 2023 7:43:46 pm                              #
# Modified By: Viraj Bagal (viraj.bagal@synapsica.com)                         #
# -----                                                                        #
# Copyright (c) 2023 Synapsica                                                 #
################################################################################
from fastapi import FastAPI, UploadFile, File
from utils import qa_utils, summary_utils
from dotenv import load_dotenv
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)-8s - %(process)d - %(levelname)-7s [%(filename)s:%(lineno)d] - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    filename="logs/app.log",
    level=logging.INFO,
)
logger = logging.getLogger("root")

load_dotenv()
app = FastAPI()


@app.post("/upload_file")
async def upload_pdf(file: UploadFile = File(...)):
    content = await file.read()
    logger.info(f"Received {file.filename} at upload_pdf endpoint")
    with open("./received_files/" + file.filename, "wb") as f:
        f.write(content)
    global retriever
    retriever = qa_utils.prepare_files_for_qa("./received_files/" + file.filename)
    if isinstance(retriever, str):
        return {"status": retriever}
    return {"status": "Success"}


@app.post("/prepare_yt_video_for_qa")
async def prepare_yt_video(yt_url):
    logger.info(f"{yt_url} YT URL received at prepare_yt_video_for_qa endpoint")
    global retriever
    retriever = qa_utils.prepare_yt_video_for_qa(yt_url)
    if isinstance(retriever, str):
        return {"status": retriever}
    return {"status": "Success"}


@app.post("/ask_question")
async def ask_question(question):
    logger.info(f"Question received at ask_question endpoint: {question}")
    admin_prompt = "Following is a question, answer it only based on the document. If answer is not available, respond with 'Answer not found in document'. Do not generate any response other than based on document. Here is the question: "
    question = admin_prompt + question
    answer = retriever.run(question)
    logger.info("Answer generated \n \n")
    return {"response": answer}


@app.post("/summarize_file")
async def summarise_file(file: UploadFile = File(...)):
    content = await file.read()
    logger.info(f"Received {file.filename} at summarize_file endpoint")
    with open("./received_files/" + file.filename, "wb") as f:
        f.write(content)
    summary = summary_utils.summarize_file("./received_files/" + file.filename, output_format)
    return {"response": summary}


@app.post("/set_output_format")
async def set_output_format(format):
    logger.info(f"{format} output format received at set_output_format endpoint")
    global output_format
    output_format = format
    return {"status": "Successful"}


@app.post("/summarize_yt")
async def summarise_yt_video(yt_url):
    logger.info(f"{yt_url} YT URL received at summarise_yt_video endpoint")
    summary = summary_utils.summarize_youtube_video(yt_url, output_format)
    return {"response": summary}
