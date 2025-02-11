from transformers import MarianMTModel, MarianTokenizer
from flask import Flask, request, jsonify
from langdetect import detect  # Language detection

app = Flask(__name__)

# Function to load MarianMT model
def load_model(target_language):
    model_name = f'Helsinki-NLP/opus-mt-en-{target_language}'  # Translate from detected language to target_language
    model = MarianMTModel.from_pretrained(model_name)
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    return model, tokenizer

# Route to handle translation
@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text = data['text']
    target_language = data['targetLanguage']

    # Detect the language of the input text
    detected_language = detect(text)

    # Only accept the languages you want
    allowed_languages = ['ar', 'en', 'fr', 'zh', 'pt', 'es']  # Arabic, English, French, Mandarin, Portuguese, Spanish
    if detected_language not in allowed_languages:
        return jsonify({"error": "Language not supported for translation."})

    model, tokenizer = load_model(target_language)

    # Encode and translate the text
    inputs = tokenizer.encode(text, return_tensors="pt")
    translated = model.generate(inputs, max_length=100)
    translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)

    return jsonify({
        "detectedLanguage": detected_language,
        "translatedText": translated_text
    })

if __name__ == '__main__':
    app.run(debug=True)



if __name__ == '__main__':
    app.run(debug=True)

