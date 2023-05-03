################################################################################
# File: form.py                                                                #
# Project: Spindle                                                             #
# Created Date: Monday, 1st May 2023 10:38:44 pm                               #
# Author: Viraj Bagal (viraj.bagal@synapsica.com)                              #
# -----                                                                        #
# Last Modified: Wednesday, 3rd May 2023 1:16:26 pm                            #
# Modified By: Viraj Bagal (viraj.bagal@synapsica.com)                         #
# -----                                                                        #
# Copyright (c) 2023 Synapsica                                                 #
################################################################################
import streamlit as st

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


twitter_follow_html = """
<a href="https://twitter.com/viraj_bagal" class="twitter-follow-button" data-show-count="false">Follow @VirajBagal</a><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
"""

linkedin_profile_html = """
<script src="https://platform.linkedin.com/badges/js/profile.js" async defer type="text/javascript"></script>
<div class="badge-base LI-profile-badge" data-locale="en_US" data-size="medium" data-theme="light" data-type="VERTICAL" data-vanity="virajbagal" data-version="v1"></div>
"""

set_page_title("Contact")

with st.sidebar:
    st.components.v1.html(linkedin_profile_html, height=300)
    st.components.v1.html(twitter_follow_html, height=100)


contact_form = """
<form action="https://formsubmit.co/virajbagal12@gmail.com" method="POST">
     <input type="hidden" name="_captcha" value="false">
     <input type="text" name="name" placeholder="Your name" required>
     <input type="email" name="email" placeholder="Your email" required>
     <textarea name="message" placeholder="Your message here"></textarea>
     <button type="submit">Send</button>
</form>
"""

colT1, colT2 = st.columns([1, 3])
with colT2:
    st.title(":orange[InsightAI] :sunglasses:")
colT1, colT2 = st.columns([1, 6])
with colT2:
    st.subheader("Understand content quickly with :blue[AI Summarization and Interactive Q&A]")
    st.caption("Supports :blue[PNGs, JPGs, Docs, PDFs, Youtube Videos]")

st.text("")
st.text("")
st.markdown(contact_form, unsafe_allow_html=True)


# Use Local CSS File
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style/style.css")
