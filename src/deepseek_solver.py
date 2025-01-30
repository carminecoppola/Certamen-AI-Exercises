# Invia esercizi a DeepSeek e raccoglie le risposte
import requests
import json
import os


#1-Passo come prompt a deepseek il campo descrizione del primo esercizio genrato da openAI
#2-Richiedo in output il codice di risoluzione dell'esercizio



# URL e API Key per DeepSeek
DEEPSEEK_API_URL = "https://api.deepseek.com/solve"
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")



#Leggo i dati mock di GPT per p
def load_mock_exercises():
    """
    Carica la lista di esercizi dal file JSON locale generato da OpenAI.

    Ritorna:
        list: Lista di esercizi con nome, descrizione, codice e test.
    """
    try:
        with open("../mock-data/responseOpenAI.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            print("\nEsercizi generati da OpenAI:")
            print("\nEs0) Desc: ", data["exercises"][0]["description"])



        return data.get("exercises", [])  # Empty list se non trova la chiave "exercises"
    except Exception as e:
        print(f"Errore nel caricamento del file JSON di OpenAI: {e}")
        return []


def get_solution_from_deepseek_local():
    """
    Invia la descrizione del primo esercizio del JSON mockato a DeepSeek e ottiene il codice di risoluzione.

    Ritorna:
        str: Il codice di risoluzione dell'esercizio da DeepSeek.
    """
    exercises = load_mock_exercises()  # Carica la lista di esercizi dal JSON locale

    print("\nexercises:", exercises)

    if not exercises:
        raise ValueError("Nessun esercizio trovato nel file JSON locale.")

    if "description" not in exercises[0]:
        raise ValueError("La descrizione dell'esercizio è mancante.")

    description = exercises[0]["description"]  # Prende la descrizione del primo esercizio

    # Prepara la richiesta per DeepSeek
    payload = {"query": description}
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers)
        response_data = response.json()

        # Estrai il codice dalla risposta
        solution_code = response_data.get("solution_code", "Codice non trovato.")

        return solution_code

    except Exception as e:
        print(f"Errore nella chiamata a DeepSeek: {e}")
        return "Errore nella chiamata a DeepSeek."