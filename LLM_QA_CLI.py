import google.generativeai as genai
import re
import os

# --- CONFIGURATION ---
# PASTE YOUR API KEY BELOW INSIDE THE QUOTES
API_KEY = "PASTE_YOUR_API_KEY_HERE" 

def configure_genai():
    """Configures the AI model with the API key."""
    if API_KEY == "PASTE_YOUR_API_KEY_HERE":
        print("ERROR: You must paste your Google API Key in the code first!")
        return None
    
    genai.configure(api_key=API_KEY)
    # Using the standard Gemini Flash model for speed
    model = genai.GenerativeModel('gemini-1.5-flash')
    return model

def preprocess_input(text):
    """
    Performs basic NLP preprocessing:
    1. Lowercasing
    2. Removing punctuation
    3. Basic Tokenization (splitting by whitespace)
    """
    # 1. Lowercase
    text = text.lower()
    
    # 2. Remove punctuation using Regex (keeps only words and spaces)
    text = re.sub(r'[^\w\s]', '', text)
    
    # 3. Tokenization (for display/logging purposes)
    tokens = text.split()
    
    return text, tokens

def get_ai_response(model, prompt):
    """Sends the processed prompt to the LLM."""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"API Error: {str(e)}"

def main():
    print("="*50)
    print("NLP Q&A SYSTEM - CLI MODE")
    print("="*50)
    
    model = configure_genai()
    if not model:
        return

    while True:
        user_input = input("\nAsk a question (or type 'exit' to quit): ")
        
        if user_input.lower() == 'exit':
            print("Exiting system...")
            break
        
        # Step 1: Preprocessing
        processed_text, tokens = preprocess_input(user_input)
        
        print(f"\n[Debug] Preprocessed: {processed_text}")
        print(f"[Debug] Tokens: {tokens}")
        print("-" * 30)
        print("Thinking...")

        # Step 2: AI Generation
        answer = get_ai_response(model, user_input)
        
        # Step 3: Output
        print("\n>> AI Answer:")
        print(answer)
        print("="*50)

if __name__ == "__main__":
    main()