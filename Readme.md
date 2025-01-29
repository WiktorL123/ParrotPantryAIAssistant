# 🥜 Parrot Hybrid Generator & Vet Assistant 🏥  

## 👀 Opis Projektu  
**Parrot Hybrid Generator & Vet Assistant** to aplikacja webowa, która pozwala na:  
- ✨ Generowanie realistycznych obrazów hybrydowych papug na podstawie opisu tekstowego.  
- 🖼️ Tworzenie obrazu potomka papug na podstawie przesłanych zdjęć rodziców.  
- 📝 Wirtualne porady weterynaryjne na podstawie opisu problemu zdrowotnego papugi.  

## 🚀 Technologie  
- **Frontend**: HTML, CSS, JavaScript  
- **Backend**: Flask (Python)  
- **AI Models**: OpenAI GPT-4 (porady weterynaryjne), DALL·E (generowanie obrazów), Hugging Face (klasyfikacja obrazów)  
- **Hosting**: Flask Server  

---

## 🔧 Instalacja i Uruchomienie  

### 1. Klonowanie repozytorium  
```sh  
git clone https://github.com/your-repo.git  
cd your-repo  
```

### 2. Instalacja zależności  
Upewnij się, że masz zainstalowanego **Pythona 3.8+**, następnie:  
```sh  
pip install -r requirements.txt  
```

### 3. Ustawienie zmiennych środowiskowych  
W katalogu głównym projektu utwórz plik `.env` i dodaj:  
```ini  
OPENAI_API_KEY=your-openai-key  
HUGGINGFACE_API_TOKEN=your-huggingface-token  
```

### 4. Uruchomienie aplikacji  
```sh  
python app.py  
```
Aplikacja będzie dostępna pod adresem: **http://127.0.0.1:5000**

---

## 🖥️ Funkcjonalności  

### 👉 1. Generowanie papug z opisu tekstowego  
📏 Użytkownik podaje krótki opis papugi hybrydowej, a model AI generuje obraz.  
**Przykładowy prompt**:  
> "Wygeneruj papugę będącą potomkiem ara i kakadu o kolorowym upierzeniu."  

### 👉 2. Generowanie papug ze zdjęć  
📎 Użytkownik przesyła **2 zdjęcia papug**, a model AI tworzy realistyczną hybrydę ich cech.  
**Wykorzystane modele**:  
- Hugging Face → Klasyfikacja papug  
- OpenAI DALL·E → Generowanie potomka  

### 👉 3. Asystent Weterynaryjny  
💼 Użytkownik opisuje problem zdrowotny papugi, a AI analizuje sytuację i sugeruje kroki leczenia.  
**Przykładowe zapytanie**:  
> "Moja papuga kicha i ma wydzielinę z nosa, co robić?"  
AI zwróci potencjalne przyczyny i zalecenia.  

---

## 🌍 Struktura Plików  
```
📂 src  
🗾️ main.py                   # Główny serwer Flask  
📃 .env                     # Klucze API (niewidoczne w repozytorium)  
📃 requirements.txt          # Zależności projektu  
📂 templates              # Pliki HTML  
   📃 index.html            # Strona główna  
📂 static                 # Zasoby frontendowe  
   📃 style.css             # Stylizacja  
   📃 script.js             # Obsługa interakcji  
```

---

## 🔄 Przyszłe Rozszerzenia  
- 🏛️ **Interaktywna baza danych papug** – użytkownicy mogą dodawać własne wpisy  
- 📂 **Historia konsultacji weterynaryjnych** – zapis poprzednich porad  
- 🌿 **Lepsza personalizacja obrazów AI**  

📧 **Masz pomysł?** Otwórz issue lub stwórz pull request! 🤝  

---

## 📚 Licencja  
MIT License – możesz swobodnie używać, modyfikować i rozwijać projekt.  

🚀 **Wesprzyj rozwój projektu!** ✨ Jeśli podoba Ci się ta aplikacja, zostaw ⭐ na GitHub!

