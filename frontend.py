################################################################################
# File: frontend.py                                                            #
# Project: Spindle                                                             #
# Created Date: Thursday, 27th April 2023 8:40:12 pm                           #
# Author: Viraj Bagal (viraj.bagal@synapsica.com)                              #
# -----                                                                        #
# Last Modified: Sunday, 30th April 2023 9:37:14 am                            #
# Modified By: Viraj Bagal (viraj.bagal@synapsica.com)                         #
# -----                                                                        #
# Copyright (c) 2023 Synapsica                                                 #
################################################################################
import streamlit as st
import requests
import logging

logger = logging.getLogger("root")


## remove default streamlit styles
hide_streamlit_style = """
                <style>
                div[data-testid="stToolbar"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stDecoration"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stStatusWidget"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                #MainMenu {
                visibility: hidden;
                height: 0%;
                }
                header {
                visibility: hidden;
                height: 0%;
                }
                footer {
                visibility: hidden;
                height: 0%;
                }
                </style>
                """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def get_answer(text):
    url = f"http://127.0.0.1:8000/ask_question?question={text}"
    payload = {}
    files = {}
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    return eval(response.text)["response"]


@st.cache_data(show_spinner=False)
def send_prepare_qa_request(uploaded_file=None, yt_url=None):
    headers = {}
    payload = {}
    files = {}
    if uploaded_file:
        url = "http://127.0.0.1:8000/upload_file"
        bytes_data = uploaded_file.getvalue()
        files = [("file", (uploaded_file.name, bytes_data, "application/pdf"))]
    elif yt_url:
        url = f"http://127.0.0.1:8000/prepare_yt_video_for_qa?yt_url={yt_url}"
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    return eval(response.text)["status"]


# @st.cache_data(show_spinner=False)
def send_summarize_request(uploaded_file=None, yt_url=None):
    payload = {}
    headers = {}
    files = {}
    if uploaded_file:
        url = "http://127.0.0.1:8000/summarize_file"
        bytes_data = uploaded_file.getvalue()
        files = [("file", (uploaded_file.name, bytes_data, "application/pdf"))]
    elif yt_url:
        url = f"http://127.0.0.1:8000/summarize_yt?yt_url={yt_url}"
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    return eval(response.text)["response"]


@st.cache_data(show_spinner=False)
def set_output_format(output_format):
    url = f"http://127.0.0.1:8000/set_output_format?format={output_format}"
    payload = {}
    files = {}
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    return eval(response.text)["status"]


colT1, colT2 = st.columns([1, 3])
with colT2:
    st.title(":orange[TextAssistant] :sunglasses:")
colT1, colT2 = st.columns([1, 5])
with colT2:
    st.subheader("Understand content quickly with :blue[AI Summarization and Interactive Q&A]")
    st.caption("Supports :blue[Docs, PDFs, Youtube Videos]")

st.text("")
st.text("")
category = st.radio("Run AI on?", ("", "File", "Youtube video"), horizontal=True)
uploaded_file = None
yt_url = None
is_supported = False
if category == "File":
    uploaded_file = st.file_uploader("Choose a File")
    if uploaded_file:
        file_name = uploaded_file.name
        extension = file_name.split(".")[-1]
        allowed_file_types = ["doc", "docx", "pdf"]
        is_supported = extension in allowed_file_types
        if not is_supported:
            st.error(f"This file format is not supported. Please upload either of {', '.join(allowed_file_types)}")
elif category == "Youtube video":
    yt_url = st.text_input("Enter Youtube video URL")

if category != "" and is_supported and (uploaded_file or yt_url):
    task = st.radio("Which task do you want the AI to do?", ("", "Summarize", "Q&A"), horizontal=True)
    if task == "Q&A":
        st.write("Preparing the AI for Q&A...")
        response = send_prepare_qa_request(uploaded_file=uploaded_file, yt_url=yt_url)
        if response == "Success":
            st.write("The AI is ready!")
            title = st.text_input("Enter question here")
            if st.button("Submit"):
                answer = get_answer(title)
                st.info(answer)
        else:
            st.error(f":red[{response}]")
        logger.info("Completed the request \n \n")
    elif task == "Summarize":
        output_format = st.radio(
            "What output format?", ("", "One Sentence", "Bullet points", "Short", "Long"), horizontal=True
        )
        if output_format != "":
            st.write("Summarising the input...")
            response = set_output_format(output_format)
            if response == "Successful":
                response = send_summarize_request(uploaded_file=uploaded_file, yt_url=yt_url)
                if response != "Sorry! Too long":
                    st.info(response)
                else:
                    st.error(response)
                logger.info("Completed the request \n \n")
