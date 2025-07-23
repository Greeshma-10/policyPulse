import streamlit as st
import requests
import re

# --- Page config ---
st.set_page_config(page_title="PolicyPulse Chatbot", layout="wide")

st.markdown("""
    <style>
        body, .stApp {
            background-color: #FFEDF3;
            font-family: 'Segoe UI', sans-serif;
        }

        .chatbox {
            max-height: 75vh;
            overflow-y: auto;
            padding-right: 10px;
        }

        .message-container {
            display: flex;
            margin-bottom: 15px;
            width: 100%;
        }

        .sender {
            justify-content: flex-end;
        }

        .receiver {
            justify-content: flex-start;
        }

        .message-bubble {
            max-width: 70%;
            padding: 15px 20px;
            border-radius: 20px;
            font-size: 16px;
            font-weight: bold;
            line-height: 1.6;
            color: #000000;
            white-space: pre-wrap;
        }

        .sender .message-bubble {
            background-color: #56DFCF;
            border-bottom-right-radius: 0;
        }

        .receiver .message-bubble {
            background-color: #ADEED9;
            border-bottom-left-radius: 0;
        }

        .input-container {
            position: fixed;
            bottom: 20px;
            left: 0;
            right: 0;
            padding: 10px 20px;
            background-color: #FFEDF3;
        }

        .input-box {
            width: 100%;
        }

        .center-heading h2 {
            text-align: center;
            color: #0ABAB5;
            font-weight: 700;
            font-size: 28px;
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# --- Session state ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Title ---
st.markdown("<div class='center-heading'><h2>🧠 PolicyPulse Chat</h2></div>", unsafe_allow_html=True)

# --- Chat messages display ---
chat_box = st.empty()
with chat_box.container():
    st.markdown('<div class="chatbox">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        # Format bot reply to remove * and bold headers
        content = msg["content"]
        if msg["role"] == "bot":
            content = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", content)  # Bold **text**
            content = re.sub(r"\*(.*?)\*", r"<b>\1</b>", content)      # Bold *text*
            content = re.sub(r"\n#+\s*(.*?)\n", r"\n<b>\1</b>\n", content)  # Bold headings if any

        css_class = "sender" if msg["role"] == "user" else "receiver"
        st.markdown(
            f"""
            <div class="message-container {css_class}">
                <div class="message-bubble">{content}</div>
            </div>
            """, unsafe_allow_html=True
        )
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("""
    <script>
        window.scrollTo(0, document.body.scrollHeight);
    </script>
    """, unsafe_allow_html=True)

# --- Input box ---
with st.container():
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("Type your message...", key="chat_input", label_visibility="collapsed")
        submit = st.form_submit_button("Send")

        if submit and user_input.strip():
            st.session_state.messages.append({"role": "user", "content": user_input})

            try:
                res = requests.post("http://127.0.0.1:5000/chat", json={"message": user_input})
                if res.status_code == 200:
                    bot_reply = res.json()["response"]
                else:
                    bot_reply = "Something went wrong with the server."
            except Exception as e:
                bot_reply = f"API Error: {str(e)}"

            st.session_state.messages.append({"role": "bot", "content": bot_reply})
            st.rerun()