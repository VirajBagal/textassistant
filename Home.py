################################################################################
# File: frontend.py                                                            #
# Project: Spindle                                                             #
# Created Date: Thursday, 27th April 2023 8:40:12 pm                           #
# Author: Viraj Bagal (viraj.bagal@synapsica.com)                              #
# -----                                                                        #
# Last Modified: Thursday, 4th May 2023 12:52:09 pm                            #
# Modified By: Viraj Bagal (viraj.bagal@synapsica.com)                         #
# -----                                                                        #
# Copyright (c) 2023 Synapsica                                                 #
################################################################################
import streamlit as st
import requests
import logging
import logging
from utils import utils

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


def set_page_title(title):
    st.sidebar.markdown(
        unsafe_allow_html=True,
        body=f"""
        <iframe height=0 srcdoc="<script>
            const title = window.parent.document.querySelector('title') \
                
            const oldObserver = window.parent.titleObserver
            if (oldObserver) {{
                oldObserver.disconnect()
            }} \

            const newObserver = new MutationObserver(function(mutations) {{
                const target = mutations[0].target
                if (target.text !== '{title}') {{
                    target.text = '{title}'
                }}
            }}) \

            newObserver.observe(title, {{ childList: true }})
            window.parent.titleObserver = newObserver \

            title.text = '{title}'
        </script>" />
    """,
    )


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


def set_output_format(output_format):
    url = f"http://127.0.0.1:8000/set_output_format?format={output_format}"
    payload = {}
    files = {}
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    return eval(response.text)["status"]


twitter_follow_html = """
<a href="https://twitter.com/viraj_bagal" class="twitter-follow-button" data-show-count="false">Follow @VirajBagal</a><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
"""

linkedin_profile_html = """
<script src="https://platform.linkedin.com/badges/js/profile.js" async defer type="text/javascript"></script>
<div class="badge-base LI-profile-badge" data-locale="en_US" data-size="medium" data-theme="light" data-type="VERTICAL" data-vanity="virajbagal" data-version="v1"></div>
"""

with open("style/main.css") as f:
    st.markdown(f"""<style>{f.read()}</style>""", unsafe_allow_html=True)

set_page_title("Home")

with st.sidebar:
    st.components.v1.html(twitter_follow_html, height=50)
    st.components.v1.html(linkedin_profile_html, height=300)

colT1, colT2 = st.columns([1, 3])
with colT2:
    st.title(":orange[InsightAI] :sunglasses:")
colT1, colT2 = st.columns([1, 6])
with colT2:
    st.subheader("Understand content quickly with :blue[AI Summarization and Interactive Q&A]")
    st.caption("Supports :blue[PNGs, JPGs, Docs, PDFs, Youtube Videos]")

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
        allowed_file_types = ["doc", "docx", "pdf", "jpg", "png"]
        is_supported = extension in allowed_file_types
        if not is_supported:
            st.error(f"This file format is not supported. Please upload either of {', '.join(allowed_file_types)}")
elif category == "Youtube video":
    yt_url = st.text_input("Enter Youtube video URL")
    yt_url = utils.convert_from_mobile_url(yt_url)
    st.components.v1.iframe(f"""{yt_url.replace("watch?v=", "embed/")}""", scrolling=True, height=350)
    is_supported = True

if category != "" and is_supported and (uploaded_file or yt_url):
    task = st.radio("Which task do you want the AI to do?", ("", "Summarize", "Q&A"), horizontal=True)
    if task == "Q&A":
        with st.spinner("Preparing the AI for Q&A..."):
            response = send_prepare_qa_request(uploaded_file=uploaded_file, yt_url=yt_url)
        if response == "Success":
            title = st.text_input("Enter question here")
            if st.button("Submit"):
                with st.spinner("AI is searching..."):
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
            response = set_output_format(output_format)
            if response == "Successful":
                with st.spinner("Summarising the input..."):
                    response = send_summarize_request(uploaded_file=uploaded_file, yt_url=yt_url)
                if response not in [
                    "Sorry! Too long. Actually, it can even summarise extremely long contents, but because this service is free, the current limit is ~7500 words. Roughly around 25-30 min video. You can try Q&A on this content.",
                    "Sorry! Too long. Actually, it can even summarise extremely long contents, but because this service is free, the current limit is ~7500 words. You can try Q&A on this content.",
                    "File cannot be processed",
                    "Video cannot be processed",
                ]:
                    st.info(response)
                else:
                    st.error(f":red[{response}]")
                logger.info("Completed the request \n \n")
