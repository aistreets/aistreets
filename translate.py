from transformers import MarianMTModel, MarianTokenizer
from flask import Flask, request, jsonify
from langdetect import detect  # Import langdetect for language detection

app = Flask(__name__)

# Function to load MarianMT model
def load_model(target_language):
    model_name = f'Helsinki-NLP/opus-mt-en-{target_language}'  # Translate from detected language to target_language
    print(f"Loading model: {model_name}")  # Debugging line
    model = MarianMTModel.from_pretrained(model_name)
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    return model, tokenizer

# Route to handle translation
@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    print(f"Received data: {data}")  # Debugging line

    text = data['text']
    target_language = data['targetLanguage']

    # Detect the language of the input text
    detected_language = detect(text)
    print(f"Detected language: {detected_language}")  # Debugging line

    allowed_languages = ['ar', 'en', 'fr', 'zh', 'pt', 'es']
    if detected_language not in allowed_languages:
        print(f"Language not supported: {detected_language}")  # Debugging line
        return jsonify({"error": "Language not supported for translation."})

    model, tokenizer = load_model(target_language)

    # Encode and translate the text
    inputs = tokenizer.encode(text, return_tensors="pt")
    translated = model.generate(inputs, max_length=100)
    translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
    
    print(f"Translated text: {translated_text}")  # Debugging line

    return jsonify({
        "detectedLanguage": detected_language,
        "translatedText": translated_text
    })

if __name__ == '__main__':
    app.run(debug=True)
