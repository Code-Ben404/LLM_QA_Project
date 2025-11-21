from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import re
import os

app = Flask(__name__)

# ==========================================
# 🛑 PASTE YOUR API KEY BELOW 🛑
# ==========================================
API_KEY = "AIzaSyA3DlxfypsyzI4L7uJ2ZMx5oYFDJ5pOWV8"

# --- DYNAMIC MODEL FINDER ---
def configure_and_get_model():
    if API_KEY == "PASTE_YOUR_API_KEY_HERE":
        print("CRITICAL ERROR: API Key is missing.")
        return None

    genai.configure(api_key=API_KEY)
    
    try:
        # Ask Google what models are available for THIS key
        print("Searching for available models...")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"Found valid model: {m.name}")
                # Return the first valid model we find (e.g., models/gemini-pro)
                return genai.GenerativeModel(m.name)
                
    except Exception as e:
        print(f"Error listing models: {e}")
    
    # Absolute fallback if search fails
    print("Search failed, forcing gemini-1.5-flash")
    return genai.GenerativeModel('gemini-1.5-flash')

# Initialize the model ONCE when app starts
model = configure_and_get_model()

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
        return jsonify({"error": "API Key is missing or Invalid in app.py!"})

    try:
        data = request.get_json()
        question = data.get('question', '')
        
        if not question: 
            return jsonify({"error": "No question provided"})

        processed_text = preprocess_input(question)
        
        # Generate Answer
        response = model.generate_content(question)
        answer_text = response.text

        return jsonify({
            "processed": processed_text,
            "answer": answer_text
        })

    except Exception as e:
        return jsonify({"error": f"AI Error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
