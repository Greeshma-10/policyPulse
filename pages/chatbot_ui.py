import streamlit as st
import requests

# --- Page config ---
st.set_page_config(page_title="PolicyPulse Chatbot", layout="wide")
st.markdown("""
    <style>
        body, .stApp {
            background-color: #FFEDF3;
        }
        .message-container {
            display: flex;
            margin-bottom: 10px;
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
            padding: 10px 15px;
            border-radius: 20px;
            color: black;
            font-size: 16px;
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
        if msg["role"] == "user":
            st.markdown(
                f"""
                <div class="message-container sender">
                    <div class="message-bubble">{msg['content']}</div>
                </div>
                """, unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div class="message-container receiver">
                    <div class="message-bubble">{msg['content']}</div>
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