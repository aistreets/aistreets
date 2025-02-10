// Speech Recognition Setup (using Web Speech API)
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.continuous = true; // Keeps recognizing until manually stopped
recognition.lang = 'en-US'; // Default language (you can set it to any language code)

const startButton = document.getElementById("start-recording");
const outputDiv = document.getElementById("output");

startButton.addEventListener('click', function() {
    // Start Speech Recognition
    recognition.start();
    startButton.disabled = true; // Disable the button once clicked
    startButton.textContent = "Listening...";
});

// When Speech Recognition detects speech
recognition.onresult = function(event) {
    const lastResult = event.results[event.results.length - 1];
    const spokenText = lastResult[0].transcript;

    // Display the spoken text
    outputDiv.textContent = `You said: ${spokenText}`;

    // Translate the spoken text to another language (e.g., Spanish)
    translateText(spokenText, 'es');  // Translating to Spanish as an example
};

// Handle any errors during recognition
recognition.onerror = function(event) {
    outputDiv.textContent = "Error: " + event.error;
    startButton.disabled = false;
    startButton.textContent = "Start Recording"; // Re-enable the button
};

// Stop the recognition process when it's done
recognition.onend = function() {
    startButton.disabled = false;
    startButton.textContent = "Start Recording"; // Re-enable the button after stop
};

// Translation function
async function translateText(text, targetLang) {
    const apiKey = 'YOUR_TRANSLATION_API_KEY'; // You’ll need an API key from a translation service
    const url = `https://api.example.com/translate?text=${encodeURIComponent(text)}&targetLang=${targetLang}&key=${apiKey}`;

    const response = await fetch(url);
    const data = await response.json();
    outputDiv.textContent = `Translated: ${data.translatedText}`;
}
