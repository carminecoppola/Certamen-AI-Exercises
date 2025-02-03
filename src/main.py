from exercise_generator import generate_exercises_from_openai
from src.openrouter import create_prompts, query_deepseek, save_output_to_json

def main():
    print("Hello World!")

    # FASE 1: Creo gli esercizi con OpenAI
    # (commentato sennò ogni volta viene generato un nuovo output e il prof paga)
    # generate_exercises_from_openai()


    # FASE 2: Creo il prompt per OpenRouter
    prompts = create_prompts()

    if not prompts:
        print("Nessun esercizio trovato.")
        return

    prompt = prompts[0]  # Prendi solo il primo esercizio per test
    print(f"\nRichiedendo soluzione per: {prompt}\n")

    response_data = query_deepseek(prompt)

    if response_data:
        solution = {
            "exercise": "Esercizio 1",
            "prompt": prompt,
            "solution": response_data
        }
        save_output_to_json([solution])

if __name__ == "__main__":
    main()
