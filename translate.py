from googletrans import Translator  # Google Translate library
from flask import Flask, request, jsonify

app = Flask(__name__)

# Initialize the Translator object from googletrans
translator = Translator()

# Route to handle translation
@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text = data['text']  # Get the text from the frontend
    target_language = data['targetLanguage']  # Get the target language

    # Translate the text using Google Translate API
    translated_text = translator.translate(text, dest=target_language).text
    
    return jsonify({
        "translatedText": translated_text  # Send the translated text back to the frontend
    })

if __name__ == '__main__':
    app.run(debug=True)



if __name__ == '__main__':
    app.run(debug=True)

