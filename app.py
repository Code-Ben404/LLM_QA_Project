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
    # CHANGED MODEL TO 'gemini-pro' (More stable)
    model = genai.GenerativeModel('gemini-pro')
else:
    model = None
    print("WARNING: API Key is missing. The app will not work until you add it.")

def preprocess_input(text):
    """
    Basic NLP Preprocessing:
    1. Convert to lowercase
    2. Remove punctuation (keep only words and spaces)
    """
    if not text: return ""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

@app.route('/')
def index():
    # Renders the frontend HTML file
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    # 1. Check if API Key is set
    if not model:
        return jsonify({
            "error": "API Key is missing in app.py! Please open app.py and paste your Google API Key."
        })

    try:
        # 2. Get data from Frontend
        data = request.get_json()
        question = data.get('question', '')
        
        if not question:
            return jsonify({"error": "No question provided"})

        # 3. Preprocessing (NLP Step)
        processed_text = preprocess_input(question)
        
        # 4. Send to LLM (AI Step)
        response = model.generate_content(question)
        answer_text = response.text

        # 5. Return Data to Frontend
        return jsonify({
            "processed": processed_text,
            "answer": answer_text
        })

    except Exception as e:
        return jsonify({"error": f"AI Error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
