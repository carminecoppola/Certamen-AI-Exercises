import json
import os
import openai

# Legge la chiave API da variabile d'ambiente(va impostata)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

#Diventerà la funzione principale quando avremo la key
def generate_exercises_from_openai():
    """
    Genera una lista di esercizi utilizzando l'API di OpenAI.
    """
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY non trovata. Assicurati di impostare la variabile d'ambiente.")

    openai.api_key = OPENAI_API_KEY

    prompt = """Generate a set of 10 exercises (ranging from beginner to hard difficulty) in Python 
    with name, description, code, and a set of input and output to test if the given code is correct.
    Return all in JSON format."""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Usa GPT-4 o un altro modello disponibile
            messages=[{"role": "system", "content": prompt}]
        )

        # Estrarre il contenuto JSON dalla risposta
        exercises_json = response["choices"][0]["message"]["content"].strip()
        exercises = json.loads(exercises_json)  # Converte la stringa JSON in un dizionario

        return exercises["exercises"]

    except Exception as e:
        print(f"Errore nella chiamata OpenAI: {e}")
        return []

#Per test da dati json mock
def generate_exercises_from_mock():
    """
    Genera una lista di esercizi leggendo da un file JSON mockato.
    """
    try:
        with open("../mock-data/responseOpenAI.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            print("\nEsercizi generati da OpenAI:")
            print("Es0) Name: ", data["exercises"][0]["name"])
            print("Es0) Desc: ", data["exercises"][0]["description"])
            print("Es0) Input: ", data["exercises"][0]["tests"][0]["input"])
            print("Es0) Output: ", data["exercises"][0]["tests"][0]["output"])

        return data["exercises"]



    except Exception as e:
        print(f"Errore nel caricamento del file mockato: {e}")
        return []
