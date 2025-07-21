from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
# LangChain + Gemini
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser

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

SYSTEM_PROMPT = open("prompt.txt", "r").read()

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')

    try:
        full_prompt = SYSTEM_PROMPT + "\n\nUser Query: " + user_message
        response = llm.invoke([HumanMessage(content=full_prompt)])
        reply = parser.invoke(response)
    except Exception as e:
        reply = f"Error: {str(e)}"

    return jsonify({'response': reply})

if __name__ == '__main__':
    app.run(debug=True)