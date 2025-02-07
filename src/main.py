from exercise_generator import generate_exercises_from_openai
from openrouter import create_prompts, query_deepseek, save_output_to_json
from code_executor import detect_language # Importa le funzioni per eseguire il codice
import json

OUTPUT_FILE = "output.json"  # Nome del file JSON dove salviamo le soluzioni

def main():
    print("🚀 Avvio del programma")

    # FASE 1: Creazione degli esercizi con OpenAI (DISATTIVATA per evitare costi)
    # generate_exercises_from_openai()

    # FASE 2: Creazione del prompt per OpenRouter
    prompts = create_prompts()

    if not prompts:
        print("❌ Nessun esercizio trovato.")
        return

    prompt = prompts[0]  # Prendi solo il primo esercizio per test
    print(f"\n🔹 Richiedendo soluzione per: {prompt}\n")

    # FASE 3: Generazione della soluzione con OpenRouter
    response_data = query_deepseek(prompt)

    if response_data:
        solution = {
            "exercise": "Esercizio 1",
            "prompt": prompt,
            "solution": response_data
        }
        save_output_to_json([solution])  # Salva la soluzione in outputDeepSeek.json

if __name__ == "__main__":
    main()