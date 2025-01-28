from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv

# Załaduj klucz API z pliku .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
print(openai.api_key)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-image', methods=['POST'])
def generate_image():
    try:
        # Pobierz prompt od użytkownika
        user_prompt = request.json.get("prompt")
        print(f"Received prompt: {user_prompt}")

        # Wywołanie OpenAI Image API (dla wersji 0.28.0)
        response = openai.Image.create(
            prompt=user_prompt,  # Prompt do generowania obrazu
            n=1,                 # Liczba obrazów do wygenerowania
            size="1024x1024"     # Rozdzielczość obrazu
        )

        # Pobranie URL wygenerowanego obrazu
        image_url = response['data'][0]['url']
        print(f"Generated image URL: {image_url}")
        return jsonify({"image_url": image_url})

    except Exception as e:
        # Logowanie błędu w konsoli
        print(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
