import json
import os
import re
import json5
import openai
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Configurazione API e file di output
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OUTPUT_FILE = "output.json"


def clean_and_validate_json(response_text) :
    """Estrae e valida un JSON da un testo ricevuto da OpenAI."""
    try :
        # Rimuove eventuali delimitatori di codice ```json ... ```
        response_text = response_text.strip("```json").strip("```").strip()

        # Cerca un blocco JSON valido nel testo
        match = re.search(r"\[.*\]", response_text, re.DOTALL)
        if match :
            json_text = match.group(0)
            return json.loads(json_text)  # Prova a caricarlo come JSON
        else :
            # Se il formato è malformato, prova con json5
            return json5.loads(response_text)

    except json.JSONDecodeError :
        print("Errore: JSON non valido, tentativo con JSON5...")
        try :
            return json5.loads(response_text)  # json5 corregge piccoli errori
        except Exception as e :
            print(f"❌ Impossibile correggere il JSON: {e}")
            return None


def generate_exercises_from_openai() :
    """Genera una lista di esercizi di Python utilizzando OpenAI e salva il risultato in un file JSON."""

    if not OPENAI_API_KEY :
        raise ValueError("OPENAI_API_KEY non trovata. Assicurati di impostare la variabile d'ambiente.")

    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    prompt = """Generate a list of 10 programming exercises in JSON format. Each exercise must follow this exact structure:
    [
        {
            "name": "<A concise and clear title for the exercise>",
            "description": "<A detailed description of the exercise, specifying what needs to be implemented>",
            "input": ["<A list of example inputs that will be used to test the solution>"],
            "output": ["<A list of expected outputs corresponding to each input>"]
        },
        {... more exercises ...}
    ]

    The exercises should vary in difficulty, ranging from beginner to advanced levels, and should cover different programming concepts (e.g., loops, recursion, data structures, algorithms). The description should be clear, without unnecessary details. Ensure that the JSON output is well-formatted and valid.
    """

    try :
        print("\nGenerating exercises from OpenAI...")

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role" : "system", "content" : prompt}]
        )

        # Estrarre e pulire il contenuto JSON dalla risposta
        raw_response = response.choices[0].message.content.strip()
        print("\n\nExercises JSON (raw):\n", raw_response)

        # Pulire e validare il JSON
        exercises = clean_and_validate_json(raw_response)

        if exercises is None :
            print("❌ Errore: Il JSON ricevuto non è valido dopo la pulizia.")
            return

        # Salvare il JSON in un file
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f :
            json.dump(exercises, f, indent=4, ensure_ascii=False)

        print(f"✅ Risultato salvato in {OUTPUT_FILE}")

    except openai.OpenAIError as e :
        print(f"❌ Errore OpenAI: {e}")
    except Exception as e :
        print(f"❌ Errore imprevisto: {e}")
