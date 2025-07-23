from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import requests # Import the requests library for making HTTP calls

# Translation
from googletrans import Translator

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
# Enable CORS for all origins to allow frontend access
CORS(app)

# Retrieve Gemini API key from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# --- Translator Setup ---
# Initialize the Google Translator
translator = Translator()

# --- Load System Prompt ---
# Read the system prompt from prompt.txt file
try:
    with open("prompt.txt", "r", encoding="utf-8") as f:
        SYSTEM_PROMPT = f.read()
except FileNotFoundError:
    # Handle case where prompt.txt might be missing
    SYSTEM_PROMPT = "You are an AI assistant providing information on Indian government schemes."
    print("Warning: prompt.txt not found. Using default system prompt.")


@app.route('/chat', methods=['POST'])
def chat():
    """
    Handles incoming chat messages, translates them, gets a response from Gemini API directly,
    and translates the response back to the user's original language.
    """
    data = request.get_json()
    user_message = data.get('message')

    if not user_message:
        return jsonify({'response': "Error: No message provided."}), 400

    try:
        # Step 1: Detect the language of the incoming user message
        detected = translator.detect(user_message)
        original_lang = detected.lang

        # Step 2: Translate user's input to English if it's not already in English
        if original_lang != 'en':
            translated_input = translator.translate(user_message, src=original_lang, dest='en').text
        else:
            translated_input = user_message

        # Step 3: Prepare the request for the Gemini API
        # The Gemini API endpoint for text generation
        gemini_api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

        # Combine system prompt and user query into the content for the model
        # The model expects a list of content objects, each with a role and parts
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {"text": SYSTEM_PROMPT + "\n\nUser Query: " + translated_input}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.7, # Increased temperature to encourage more direct responses
                "topK": 1,
                "topP": 1,
                "maxOutputTokens": 2048,
                "responseMimeType": "text/plain",
            }
        }

        headers = {
            "Content-Type": "application/json"
        }

        # Make the POST request to the Gemini API
        gemini_response = requests.post(gemini_api_url, headers=headers, json=payload)
        gemini_response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)

        # Parse the JSON response from Gemini
        result = gemini_response.json()

        # Extract the text from the Gemini response
        # Check for the expected structure before accessing
        if result and 'candidates' in result and len(result['candidates']) > 0 and \
           'content' in result['candidates'][0] and 'parts' in result['candidates'][0]['content'] and \
           len(result['candidates'][0]['content']['parts']) > 0 and \
           'text' in result['candidates'][0]['content']['parts'][0]:
            english_reply = result['candidates'][0]['content']['parts'][0]['text']
        else:
            # Handle cases where the response structure is unexpected
            english_reply = "Could not get a valid response from the AI model."
            print(f"Unexpected Gemini API response structure: {result}")


        # Step 4: Translate the LLM's English reply back to the user's original language
        if original_lang != 'en':
            final_reply = translator.translate(english_reply, src='en', dest=original_lang).text
        else:
            final_reply = english_reply

    except requests.exceptions.RequestException as req_err:
        # Handle errors specifically from the requests library (e.g., network issues, bad status codes)
        final_reply = f"Network or API error: {str(req_err)}. Please check your API key and network connection."
        print(f"Requests error: {req_err}")
    except Exception as e:
        # Catch any other exceptions during the process and return an error message
        final_reply = f"An unexpected error occurred: {str(e)}. Please try again."
        # Log the error for debugging purposes
        print(f"General error processing chat message: {e}")

    # Return the final translated response as a JSON object
    return jsonify({'response': final_reply})

# Run the Flask application
if __name__ == '__main__':
    # debug=True allows for automatic reloading on code changes and provides a debugger
    app.run(debug=True)
