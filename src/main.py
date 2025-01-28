from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv
import requests
from PIL import Image

# Załaduj klucze z pliku .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Token i URL API Hugging Face
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/google/vit-base-patch16-224"

# Minimalna pewność
MIN_CONFIDENCE = 0.6

# Lista gatunków papug
VALID_PARROT_LABELS = [
    "parrot",
    "macaw",
    "cockatoo",
    "sulphur-crested cockatoo",
    "Cacatua galerita",
    "Kakatoe galerita",
    "conure",
    "lovebird",
    "budgerigar",
    "lorikeet",
    "African grey parrot"
]

headers_huggingface = {
    "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"
}

def is_valid_parrot(label):
    """
    Sprawdź, czy etykieta odpowiada gatunkowi papugi.
    """
    return any(parrot in label.lower() for parrot in VALID_PARROT_LABELS)

def classify_image(image):
    """
    Klasyfikuj obraz za pomocą Hugging Face.
    """
    try:
        response = requests.post(HUGGINGFACE_API_URL, headers=headers_huggingface, data=image.read())
        result = response.json()

        if "error" in result:
            raise Exception(f"Błąd Hugging Face: {result['error']}")

        label = result[0]['label']
        confidence = result[0]['score']
        return label, confidence

    except Exception as e:
        print(f"Error during image classification: {e}")
        return None, 0.0

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-image-text', methods=['POST'])
def generate_image_text():
    """
    Obsługa prompta tekstowego wysłanego przez użytkownika.
    """
    try:
        # Pobierz prompt od użytkownika
        user_prompt = request.json.get("prompt")
        print(f"Received prompt: {user_prompt}")

        # Wywołanie OpenAI Image API
        response = openai.Image.create(
            prompt=user_prompt,
            n=1,
            size="1024x1024"
        )

        # Pobranie URL wygenerowanego obrazu
        image_url = response['data'][0]['url']
        return jsonify({"image_url": image_url})

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/generate-image-photos', methods=['POST'])
def generate_image_photos():
    """
    Obsługa przesyłania dwóch zdjęć i generowania prompta na ich podstawie.
    """
    try:
        # Pobierz obrazy z formularza
        photo1 = request.files.get('photo1')
        photo2 = request.files.get('photo2')

        if not photo1 or not photo2:
            return jsonify({"error": "Both photos are required"}), 400

        # Klasyfikacja obrazów za pomocą Hugging Face
        label1, confidence1 = classify_image(photo1)
        label2, confidence2 = classify_image(photo2)

        # Sprawdzanie pewności i poprawności etykiet
        if confidence1 < MIN_CONFIDENCE or not is_valid_parrot(label1):
            return jsonify({"error": f"Image 1 is not a valid parrot or confidence is too low: {label1} ({confidence1:.2f})"}), 400

        if confidence2 < MIN_CONFIDENCE or not is_valid_parrot(label2):
            return jsonify({"error": f"Image 2 is not a valid parrot or confidence is too low: {label2} ({confidence2:.2f})"}), 400

        # Przygotuj prompt do generowania obrazu
        user_prompt = (
            f"You are an AI specialized in creating artistic depictions of hybrid parrots. "
            f"Combine the most distinctive features of these two parrots: "
            f"First parrot: {label1}. "
            f"Second parrot: {label2}. "
            f"Use their colors, patterns, and shapes to design a visually striking and realistic hybrid parrot. "
            f"Depict the hybrid parrot in full view with detailed plumage and vibrant colors. Use a clean and contrasting "
            f"background to make the parrot's features stand out."
        )

        # Wywołanie OpenAI Image API
        response = openai.Image.create(
            prompt=user_prompt,
            n=1,
            size="1024x1024"
        )

        # Pobierz URL wygenerowanego obrazu
        image_url = response['data'][0]['url']
        return jsonify({
            "image_url": image_url,
            "labels": {
                "image1": label1,
                "confidence1": confidence1,
                "image2": label2,
                "confidence2": confidence2
            }
        })

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
