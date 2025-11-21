from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import re
import os

app = Flask(__name__)

# ==========================================
# 🛑 PASTE YOUR API KEY BELOW 🛑
# ==========================================
API_KEY = "AIzaSyA3DlxfypsyzI4L7uJ2ZMx5oYFDJ5pOWV8"

# Configure the AI Model
if API_KEY != "PASTE_YOUR_API_KEY_HERE":
    genai.configure(api_key=API_KEY)
    # We use the standard, most reliable free model
    model = genai.GenerativeModel('gemini-pro')
else:
    model = None

def preprocess_input(text):
    if not text: return ""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    if not model:
        return jsonify({"error": "API Key is missing in app.py!"})

    try:
        data = request.get_json()
        question = data.get('question', '')
        
        if not question:
            return jsonify({"error": "No question provided"})

        processed_text = preprocess_input(question)
        
        # Send to AI
        response = model.generate_content(question)
        answer_text = response.text

        return jsonify({
            "processed": processed_text,
            "answer": answer_text
        })

    except Exception as e:
        # If we get a 429 error, tell the user to wait
        if "429" in str(e):
            return jsonify({"error": "Too many requests! Please wait 1 minute and try again."})
        return jsonify({"error": f"AI Error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
