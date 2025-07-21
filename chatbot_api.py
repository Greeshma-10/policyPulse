from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

# LangChain + Gemini
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser

# Translation
from googletrans import Translator

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# LangChain model setup
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.3
)
parser = StrOutputParser()

# Translator setup
translator = Translator()

# Load system prompt
with open("prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')

    try:
        # Step 1: Detect language
        detected = translator.detect(user_message)
        original_lang = detected.lang

        # Step 2: Translate to English if not already
        if original_lang != 'en':
            translated_input = translator.translate(user_message, src=original_lang, dest='en').text
        else:
            translated_input = user_message

        # Step 3: Construct prompt
        full_prompt = SYSTEM_PROMPT + "\n\nUser Query: " + translated_input
        response = llm.invoke([HumanMessage(content=full_prompt)])
        english_reply = parser.invoke(response)

        # Step 4: Translate back to original language
        if original_lang != 'en':
            final_reply = translator.translate(english_reply, src='en', dest=original_lang).text
        else:
            final_reply = english_reply

    except Exception as e:
        final_reply = f"Error: {str(e)}"

    return jsonify({'response': final_reply})

if __name__ == '__main__':
    app.run(debug=True)
