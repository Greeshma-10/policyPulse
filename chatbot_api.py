from flask import Flask, request, jsonify
import google.generativeai as genai
import os
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Get API key from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Load Gemini model
model = genai.GenerativeModel('gemini-1.5-flash-latest')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')

    try:
        response = model.generate_content(user_message)
        reply = response.text
    except Exception as e:
        reply = f"Error: {str(e)}"

    return jsonify({'response': reply})

if __name__ == '__main__':
    app.run(debug=True)
