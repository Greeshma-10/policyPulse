import streamlit as st
import requests
import re
import time

# --- Page config ---
st.set_page_config(page_title="PolicyPulse Chatbot", layout="wide")

st.markdown("""
    <style>
    /* New Color Palette (from https://colorhunt.co/palette/fffbde90d1ca129990096b68):
        - Background: #FFFBDE
        - Lighter Accent (selection/hover, user bubbles): #90D1CA
        - Medium Accent (buttons, borders): #129990
        - Primary Accent (headers, strong lines): #096B68

        - Card Background/Bot Bubbles: #FFFFFF (retained for contrast)
        - Text Dark: #343A40 (retained for readability)
        - Text Medium: #6C757D (retained for readability)
    */

    body, .stApp {
        background-color: #FFFBDE; /* New main background color */
        font-family: 'Segoe UI', Arial, sans-serif; /* Consistent font */
        color: #343A40; /* Dark grey text */
    }

    /* Target the main content container and remove default padding/margins for wide layout */
    .css-1d391kg, .css-1dp5yy6, .css-1r6dm1x, .css-1sp8zjk { /* Common Streamlit wrappers for wide mode */
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: unset !important; /* Ensure no max-width on these parent containers */
    }

    /* Header for Chatbot - consistent with app.py */
    .chatbot-header-container {
        background-color: #096B68; /* New primary accent for header background */
        padding: 35px 0;
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
        text-align: center;
    }

    .chatbot-header-title {
        font-size: 3.2em;
        color: #ffffff;
        font-weight: 800;
        letter-spacing: 1.8px;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }

    .chatbot-header-subtitle {
        font-size: 1.4em;
        color: #e0e0e0;
        font-weight: 400;
        margin-bottom: 0;
    }

    .chatbox {
        max-height: 65vh; /* Adjusted for header and input to provide scroll */
        overflow-y: auto;
        padding: 20px; /* Padding inside chatbox */
        border-radius: 15px;
        background-color: transparent; /* Make background transparent */
        box-shadow: none; /* Remove shadow */
        margin: 0 auto;
        max-width: 900px;
        border: none; /* Remove border as well if you want it completely invisible when empty */
        min-height: 0; /* Allow it to collapse if no content */
    }

    /* Scrollbar Styling */
    .chatbox::-webkit-scrollbar {
        width: 10px;
    }
    .chatbox::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    .chatbox::-webkit-scrollbar-thumb {
        background: #ced4da;
        border-radius: 10px;
    }
    .chatbox::-webkit-scrollbar-thumb:hover {
        background: #6C757D;
    }

    .message-container {
        display: flex;
        margin-bottom: 18px; /* Space between messages */
        width: 100%;
        align-items: flex-end;
    }

    .sender {
        justify-content: flex-end;
    }

    .receiver {
        justify-content: flex-start;
    }

    /* WhatsApp-like Message Bubble Styling */
    .message-bubble {
        max-width: 75%;
        padding: 10px 14px;
        border-radius: 12px;
        font-size: 16px;
        line-height: 1.5;
        color: #343A40;
        white-space: pre-wrap;
        word-wrap: break-word;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1); /* Keep shadows on individual bubbles */
        position: relative;
    }

    /* Sender (User) Bubble Specifics */
    .sender .message-bubble {
        background-color: #90D1CA; /* New lighter accent for user messages */
        border-bottom-right-radius: 2px;
    }

    /* Sender (User) Tail */
    .sender .message-bubble::after {
        content: '';
        position: absolute;
        bottom: 0px;
        right: -8px;
        width: 15px;
        height: 15px;
        background-color: #90D1CA; /* Match user bubble color */
        clip-path: polygon(0% 100%, 100% 100%, 100% 0%);
        border-bottom-right-radius: 2px;
    }

    /* Receiver (Bot) Bubble Specifics */
    .receiver .message-bubble {
        background-color: #FFFFFF; /* White for bot messages (card-like) */
        border-bottom-left-radius: 2px;
    }

    /* Receiver (Bot) Tail */
    .receiver .message-bubble::after {
        content: '';
        position: absolute;
        bottom: 0px;
        left: -8px;
        width: 15px;
        height: 15px;
        background-color: #FFFFFF; /* Match bot bubble color */
        clip-path: polygon(0% 0%, 0% 100%, 100% 100%);
        border-bottom-left-radius: 2px;
    }

    /* Input container styling */
    .input-container {
        position: sticky;
        bottom: 0;
        padding: 20px 0;
        background-color: #FFFBDE; /* New main background color for input area */
        border-top: 1px solid #e9ecef; /* Keep subtle border */
        box-shadow: 0 -5px 15px rgba(0,0,0,0.03);
        margin-top: 20px;
        display: flex;
        justify-content: center; /* Center the form horizontally */
        align-items: center;
        width: 100%;
    }

    .stForm {
        width: 100%;
        max-width: 900px;
        display: flex;
        gap: 15px;
        margin: 0 auto;
    }

    .stTextInput {
        flex-grow: 1;
    }

    .stTextInput>div>div>input {
        border-radius: 10px;
        border: 1px solid #ced4da;
        padding: 14px 18px;
        font-size: 1.05em;
        color: #343A40;
        background-color: #ffffff;
        box-shadow: inset 0 1px 4px rgba(0,0,0,0.08);
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }
    .stTextInput>div>div>input:focus {
        border-color: #129990; /* New medium accent on focus */
        box-shadow: inset 0 1px 4px rgba(0,0,0,0.08), 0 0 0 0.2rem rgba(18, 153, 144, 0.25);
        outline: none;
    }

    .stButton>button {
        background-color: #129990 !important; /* IMPORTANT: New medium accent for send button */
        color: white !important; /* IMPORTANT: Ensure text color is white */
        border: none;
        padding: 14px 28px;
        border-radius: 10px;
        font-weight: bold;
        font-size: 1.1em;
        transition: background-color 0.3s ease, transform 0.2s ease, box-shadow 0.3s ease;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        min-width: 120px;
    }

    .stButton>button:hover {
        background-color: #096B68 !important; /* IMPORTANT: New primary accent on hover */
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
    }

    /* Bot typing indicator */
    .typing-indicator {
        display: flex;
        justify-content: flex-start;
        align-items: center;
        margin-bottom: 20px;
    }
    .typing-indicator .message-bubble {
        background-color: #FFFFFF; /* Match bot bubble color */
        padding: 8px 12px;
        display: flex;
        align-items: center;
        width: auto;
        box-shadow: none;
        border-bottom-left-radius: 2px;
    }
    .typing-indicator .message-bubble::after {
        content: '';
        position: absolute;
        bottom: 0px;
        left: -8px;
        width: 15px;
        height: 15px;
        background-color: #FFFFFF; /* Match bot bubble color */
        clip-path: polygon(0% 0%, 0% 100%, 100% 100%);
        border-bottom-left-radius: 2px;
    }

    .typing-indicator .dot {
        width: 8px;
        height: 8px;
        background-color: #6C757D;
        border-radius: 50%;
        margin: 0 3px;
        animation: bounce 1s infinite ease-in-out;
    }
    .typing-indicator .dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-indicator .dot:nth-child(3) { animation-delay: 0.4s; }

    </style>
""", unsafe_allow_html=True)

# --- Session state ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add a welcome message if chat is new
    st.session_state.messages.append({"role": "bot", "content": "Hello! I'm PolicyPulse Chatbot, your AI assistant for government schemes. How can I help you today?"})

# --- Title ---
st.markdown(
    """
    <div class="chatbot-header-container">
        <div class="chatbot-header-title">PolicyPulse Chatbot</div>
        <div class="chatbot-header-subtitle">Your AI Assistant for Government Schemes</div>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Chat messages display ---
chat_display_col = st.columns([0.1, 0.8, 0.1])
with chat_display_col[1]:
    chat_box = st.empty()
    with chat_box.container():
        st.markdown('<div class="chatbox">', unsafe_allow_html=True)
        for msg in st.session_state.messages:
            content = msg["content"]
            if msg["role"] == "bot":
                content = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", content)
                content = re.sub(r"\*(.*?)\*", r"<b>\1</b>", content)
                content = re.sub(r"\n#+\s*(.*?)\n", r"\n<br><b>\1</b><br>\n", content)

            css_class = "sender" if msg["role"] == "user" else "receiver"
            st.markdown(
                f"""
                <div class="message-container {css_class}">
                    <div class="message-bubble">{content}</div>
                </div>
                """, unsafe_allow_html=True
            )
        if st.session_state.get("bot_typing", False):
            st.markdown("""
            <div class="typing-indicator">
                <div class="message-bubble">
                    <div class="dot"></div>
                    <div class="dot"></div>
                    <div class="dot"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("""
        <script>
            var chatbox = document.querySelector('.chatbox');
            if (chatbox) {
                chatbox.scrollTop = chatbox.scrollHeight;
            }
        </script>
        """, unsafe_allow_html=True)


# --- Input box ---
st.markdown('<div class="input-container">', unsafe_allow_html=True)
with st.container():
    with st.form(key="chat_form", clear_on_submit=True):
        input_col, button_col = st.columns([8, 2])
        with input_col:
            user_input = st.text_input("Type your message...", key="chat_input", label_visibility="collapsed")
        with button_col:
            submit_button = st.form_submit_button("Send")

        if submit_button and user_input.strip():
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.session_state.bot_typing = True
            st.rerun()

if st.session_state.get("bot_typing", False):
    time.sleep(1.5)

    try:
        last_user_message = st.session_state.messages[-1]["content"]
        res = requests.post("http://127.0.0.1:5000/chat", json={"message": last_user_message})
        if res.status_code == 200:
            bot_reply = res.json()["response"]
        else:
            bot_reply = f"Error: {res.status_code} - {res.text}"
    except requests.exceptions.ConnectionError:
        bot_reply = "Could not connect to the API. Please ensure the backend server is running."
    except Exception as e:
        bot_reply = f"An unexpected error occurred: {str(e)}"

    st.session_state.messages.append({"role": "bot", "content": bot_reply})
    st.session_state.bot_typing = False
    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)