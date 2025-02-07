import requests
import json
import os
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Configuration API &  input/output file
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
DEEPSEEK_MODEL = "deepseek/deepseek-chat"

INPUT_FILE = "output.json"
OUTPUT_FILE = "outputDeepSeek.json"


def create_prompts():
    """Legge il file JSON e genera il prompt per DeepSeek."""
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list) or not data:
            print("Errore: Nessun esercizio valido trovato nel JSON.")
            return []

        first_exercise = data[0]

        if "name" in first_exercise and "description" in first_exercise:
            prompt_text = (
                f"Esercizio: {first_exercise['name']}\n"
                f"Descrizione: {first_exercise['description']}\n"
                "Provide the solution as code, with a function that implements the required logic."
            )

            print("\nPrompt generato per DeepSeek:\n", prompt_text)
            return [prompt_text]

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
            {"role": "system", "content": "Fornisci sempre la risposta in JSON e includi il codice Python per risolvere l'esercizio."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        response_json = response.json()

        print("Risposta API DeepSeek:", json.dumps(response_json, indent=4, ensure_ascii=False))

        if "choices" in response_json and response_json["choices"]:
            return response_json
        else:
            print("Errore: Risposta API non valida.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Errore API: {e}")
        return None


def save_output_to_json(results):
    """Salva solo i campi desiderati in un file JSON."""
    try:
        filtered_results = []
        for result in results:
            exercise = result.get("exercise", "Esercizio sconosciuto")
            prompt = result.get("prompt", "Prompt non disponibile")

            # Estrarre la soluzione dall'API DeepSeek
            solution_choices = result.get("solution", {}).get("choices", [])

            if solution_choices and isinstance(solution_choices, list):
                message_content = solution_choices[0].get("message", {}).get("content", "")

                # Tentiamo di estrarre il codice Python
                solution = "Soluzione non disponibile"

                # Controlliamo prima se il contenuto è un JSON che contiene il codice
                if "```json" in message_content:
                    try:
                        json_part = message_content.split("```json")[1].split("```")[0].strip()
                        json_data = json.loads(json_part)  # Decodifica il JSON interno
                        solution = json_data.get("code", solution)  # Estrarre il codice dal JSON
                    except json.JSONDecodeError:
                        pass  # Se fallisce, proseguiamo a cercare il blocco Python

                # Se il codice è anche ripetuto nel blocco ```python```, prendiamo quello
                if "```python" in message_content:
                    solution = message_content.split("```python")[1].split("```")[0].strip()

            else:
                solution = "Soluzione non disponibile"

            filtered_results.append({
                "exercise": exercise,
                "prompt": prompt,
                "solution": solution
            })

        # Salvataggio nel file JSON
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(filtered_results, f, indent=4, ensure_ascii=False)

        print(f"Risultati salvati in {OUTPUT_FILE}")

    except Exception as e:
        print(f"Errore nel salvataggio del file JSON: {e}")
