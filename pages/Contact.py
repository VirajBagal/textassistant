################################################################################
# File: form.py                                                                #
# Project: Spindle                                                             #
# Created Date: Monday, 1st May 2023 10:38:44 pm                               #
# Author: Viraj Bagal (viraj.bagal@synapsica.com)                              #
# -----                                                                        #
# Last Modified: Thursday, 4th May 2023 8:41:42 pm                             #
# Modified By: Viraj Bagal (viraj.bagal@synapsica.com)                         #
# -----                                                                        #
# Copyright (c) 2023 Synapsica                                                 #
################################################################################
import streamlit as st

# needs to be the first streamlit command
st.set_page_config(page_title="InsightAI - Contact", page_icon=":sunglasses:", layout="centered")
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

stripe_payment_link = """
<script async
  src="https://js.stripe.com/v3/buy-button.js">
</script>

<stripe-buy-button
  buy-button-id="buy_btn_1N40hVSAlzIVpE1tBlJ5TQSO"
  publishable-key="pk_live_51N40DgSAlzIVpE1tXxSwFX62jKO17OAuiMvBN8VJwBki3RH7toe8P8qPgjjZPVhHLLr4frnbhf3rspNbXBY5rojC00OINvft4D"
>
</stripe-buy-button>
"""

# set_page_title("Contact")

with st.sidebar:
    st.subheader("Buy me a coffee :smile:")
    st.components.v1.html(stripe_payment_link, height=300)
    st.subheader("Lets Connect!")
    st.components.v1.html(twitter_follow_html, height=50)
    st.components.v1.html(linkedin_profile_html, height=300)


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
