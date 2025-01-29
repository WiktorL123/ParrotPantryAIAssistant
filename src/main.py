from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv
import requests

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/google/vit-base-patch16-224"

MIN_CONFIDENCE = 0.6

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
        user_prompt = request.json.get("prompt")
        print(f"Received prompt: {user_prompt}")

        response = openai.Image.create(
            prompt=user_prompt,
            n=1,
            size="1024x1024"
        )

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
        photo1 = request.files.get('photo1')
        photo2 = request.files.get('photo2')

        if not photo1 or not photo2:
            return jsonify({"error": "Both photos are required"}), 400

        label1, confidence1 = classify_image(photo1)
        label2, confidence2 = classify_image(photo2)

        if confidence1 < MIN_CONFIDENCE or not is_valid_parrot(label1):
            return jsonify({"error": f"Image 1 is not a valid parrot or confidence is too low: {label1} ({confidence1:.2f})"}), 400

        if confidence2 < MIN_CONFIDENCE or not is_valid_parrot(label2):
            return jsonify({"error": f"Image 2 is not a valid parrot or confidence is too low: {label2} ({confidence2:.2f})"}), 400

        user_prompt = f"""
            Na podstawie dwóch papug: {label1} i {label2}, napisz krótki tekst np "wygeneruj zdjęcie fikcyjnego potomka ary i kakadu uwzględniając charakterystyczne cechy obu" dla kolejnego prompta.
            """

        response = openai.Image.create(
            prompt=user_prompt,
            n=1,
            size="1024x1024"
        )

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

@app.route('/vet-assistant', methods=['POST'])
def vet_assistant():
    """
    Asystent weterynaryjny dla papug. Obsługuje opis problemu zdrowotnego podany przez użytkownika.
    """
    try:
        user_problem = request.json.get("problem")
        if not user_problem:
            return jsonify({"error": "Problem description is required."}), 400

        prompt = (
            f"Jesteś weterynarzem specjalizującym się w papugach Użytkownik opisał następujący problem zdrowotny swojej papugi {user_problem} "
            f"Podaj szczegółową praktyczną odpowiedź uwzględniając potencjalne przyczyny objawy do obserwacji oraz zalecane dalsze kroki Jeśli problem jest poważny zasugeruj natychmiastową konsultację z weterynarzem Nie używaj żadnych znaków specjalnych ani punktacji odpowiedź ma być sformułowana w sposób ciągły i zrozumiały"
        )

        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an AI veterinarian specialized in parrot health."},
                {"role": "user", "content": prompt}
            ]
        )

        advice = response['choices'][0]['message']['content']
        return jsonify({"advice": advice})

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
