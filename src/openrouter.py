import requests
import json
import os
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Configurazione API e file di input/output
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
DEEPSEEK_MODEL = "deepseek/deepseek-chat"

INPUT_FILE = "output.json"
OUTPUT_FILE = "outputDeepSeek.json"


def create_prompts():
    """Legge il file JSON e restituisce solo il primo esercizio sotto forma di prompt."""
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)  # Carica il JSON come una lista

        if not isinstance(data, list):  # Controlla se il JSON è una lista
            print("Errore: Il JSON non è una lista di esercizi.")
            return []

        if not data:  # Controlla se la lista è vuota
            print("Errore: Nessun esercizio trovato nel JSON.")
            return []

        first_exercise = data[0]  # Prende il primo esercizio
        if "description" in first_exercise:
            prompt_text = f"Esercizio 1: {first_exercise['description']}"
            print(prompt_text)
            return [prompt_text]  # Restituisce una lista con il primo esercizio

    except Exception as e:
        print(f"Errore nella lettura del file JSON: {e}")
        return []

def query_deepseek(prompt):
    """Invia una richiesta all'API di OpenRouter e restituisce la risposta in JSON."""
    if not OPENROUTER_API_KEY:
        raise ValueError("Errore: API Key non valida o mancante. Controlla la tua chiave.")

    API_URL = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": DEEPSEEK_MODEL,
        "messages": [
            {"role": "system", "content": "Rispondi sempre in formato JSON."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Errore API: {e}")
        return None


def save_output_to_json(results):
    """Salva solo i campi desiderati in un file JSON."""
    try:
        filtered_results = [
            {
                "exercise": result["exercise"],
                "prompt": result["prompt"],
                "solution": {
                    "choices": [
                        {
                            "content": result["solution"]["choices"][0]["message"]["content"]
                        }
                    ]
                }
            }
            for result in results
        ]

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(filtered_results, f, indent=4)

        print(f"Risultati filtrati salvati in {OUTPUT_FILE}")

    except Exception as e:
        print(f"Errore nel salvataggio del file JSON: {e}")
