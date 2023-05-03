################################################################################
# File: summary_utils.py                                                       #
# Project: Spindle                                                             #
# Created Date: Friday, 28th April 2023 8:26:49 pm                             #
# Author: Viraj Bagal (viraj.bagal@synapsica.com)                              #
# -----                                                                        #
# Last Modified: Wednesday, 3rd May 2023 6:34:00 pm                            #
# Modified By: Viraj Bagal (viraj.bagal@synapsica.com)                         #
# -----                                                                        #
# Copyright (c) 2023 Synapsica                                                 #
################################################################################
from utils import utils
from langchain.chat_models import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain

# Prompt templates for dynamic values
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

import logging

logger = logging.getLogger("root")

summary_output_options = {
    "One Sentence": """
     - Only one sentence
    """,
    "Bullet points": """
     - Bullet point format
     - Separate each bullet point with a new line
     - Each bullet point should be concise
    """,
    "Short": """
     - A few short sentences
     - Do not go longer than 4-5 sentences
    """,
    "Long": """
     - A verbose summary
     - You may do a few paragraphs to describe the transcript if needed
    """,
}


def content_summarizer(document, output_format, chain_type="stuff"):
    chat_prompt, chat_combine_prompt = create_prompts()
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    chain = load_summarize_chain(
        llm, chain_type, map_prompt=chat_prompt, combine_prompt=chat_combine_prompt, verbose=False
    )
    summary = chain.run(
        {
            "input_documents": document,
            "output_format": summary_output_options[output_format],
        }
    )
    return summary


def create_prompts():
    template = """

    You are a helpful assistant that helps summarize information.
    Your goal is to write a summary that will highlight key points.
    Do not respond with anything outside of the information. If you don't know, say, "I don't know"
    
    """
    system_message_prompt_map = SystemMessagePromptTemplate.from_template(template)

    human_template = "{text}"  # Simply just pass the text as a human message
    human_message_prompt_map = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt_map = ChatPromptTemplate.from_messages(messages=[system_message_prompt_map, human_message_prompt_map])

    template = """

    You are a helpful assistant that helps summarize information.
    Your goal is to write a summary that will highlight key points.
    Do not respond with anything outside of the information. If you don't know, say, "I don't know"

    Respond with the following format
    {output_format}

    """
    system_message_prompt_combine = SystemMessagePromptTemplate.from_template(template)

    human_template = "{text}"  # Simply just pass the text as a human message
    human_message_prompt_combine = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt_combine = ChatPromptTemplate.from_messages(
        messages=[system_message_prompt_combine, human_message_prompt_combine]
    )
    return chat_prompt_map, chat_prompt_combine


def long_content_summarizer(document, output_format):
    texts = utils.split_text(document, 2000, 0)
    summary = content_summarizer(texts, output_format, chain_type="map_reduce")
    return summary


def summarize_youtube_video(url, output_format):
    try:
        logger.info("Loading YT content")
        result = utils.load_youtube_url(url)
        logger.info("YT content loaded")
        num_tokens = utils.estimate_tokens(result[0])
        logger.info(f"Estimated tokens are {num_tokens}")
        if num_tokens > utils.REJECT_TOKENS_THRESHOLD:
            logger.info(f"Rejecting request due to large number of tokens: {num_tokens}")
            return "Sorry! Too long"
        if num_tokens > utils.LONG_VIDEO_THRESHOLD:
            logger.info("Generating summary from long_content_summarizer")
            summary = long_content_summarizer(result, output_format)
        else:
            logger.info("Generating summary from content_summarizer")
            summary = content_summarizer(result, output_format, chain_type="map_reduce")
        logger.info("Summary generated \n \n")
    except:
        logging.exception("")
        return "Video cannot be processed"
    return summary
    # audio = generate(summary)
    # save(audio, filename="trial.wav")


def summarize_file(file_path, output_format):
    try:
        logger.info("Loading file for qa")
        result = []
        if ".pdf" in file_path:
            result = utils.load_pdf(file_path)
        elif ".doc" in file_path or ".docx" in file_path:
            result = utils.load_doc(file_path)
        elif ".png" in file_path or ".jpg" in file_path:
            result = utils.load_image(file_path)
        logger.info("File loaded for qa")
        logger.info(f"Total number of pages are {len(result)}")
        total_tokens = 0
        for page in result:
            total_tokens += utils.estimate_tokens(page)
        logger.info(f"Estimated tokens are {total_tokens}")
        if total_tokens > utils.REJECT_TOKENS_THRESHOLD:
            logger.info(f"Rejecting request due to large number of tokens: {total_tokens}")
            return "Sorry! Too long"
        logger.info("Generating summary from content_summarizer")
        summary = content_summarizer(result, output_format, chain_type="map_reduce")
        logger.info("Summary generated \n \n")
    except:
        logging.exception("")
        return "File cannot be processed"
    return summary
    # audio = generate(summary)
    # save(audio, filename="trial.wav")
