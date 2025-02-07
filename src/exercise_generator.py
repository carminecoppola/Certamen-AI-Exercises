import json
import os
import openai
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Configurazione API e file di output
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OUTPUT_FILE = "output.json"


def generate_exercises_from_openai() :
    """Genera una lista di esercizi di Python utilizzando OpenAI e salva il risultato in un file JSON."""

    if not OPENAI_API_KEY :
        raise ValueError("OPENAI_API_KEY non trovata. Assicurati di impostare la variabile d'ambiente.")

    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    prompt = """Generate a set of 10 exercises (ranging from beginner to hard difficulty) in programming 
    languages like Python, C, C++, javascript with name, description, and a set of input and output to 
    test if the given code is correct. Return all in JSON format."""

    try :
        print("\nGenerating exercises from OpenAI...")

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role" : "system", "content" : prompt}]
        )

        # Estrarre e pulire il contenuto JSON dalla risposta
        exercises_json = response.choices[0].message.content.strip()
        print("\n\nExercises JSON:\n", exercises_json)

        # Convertire la stringa JSON in un dizionario
        exercises = json.loads(exercises_json)

        # Salvare il JSON in un file
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f :
            json.dump(exercises, f, indent=4, ensure_ascii=False)

        print(f"Risultato salvato in {OUTPUT_FILE}")

    except json.JSONDecodeError :
        print("Errore: Il JSON ricevuto non è valido.")
    except openai.OpenAIError as e :
        print(f"Errore OpenAI: {e}")
    except Exception as e :
        print(f"Errore imprevisto: {e}")
