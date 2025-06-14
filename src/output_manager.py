from colorama import init, Fore, Style
import json

init(autoreset=True)

class OutputManager:
    def __init__(self, save_file="results/output_llm_results.json"):
        self.all_results = []
        self.save_file = save_file

    def pretty_print_result(self, exercise, solution_code, test_results, elapsed_time):
        print(Style.BRIGHT + Fore.BLUE + "="*60)
        print(Fore.YELLOW + f"Exercise: {exercise['name']}")
        print(Fore.CYAN + f"Description: {exercise['description']}\n")
        print(Fore.GREEN + "Generated Solution:\n" + Style.RESET_ALL)
        print(Fore.WHITE + solution_code)
        print(Style.BRIGHT + Fore.BLUE + "-"*60)
        print(Fore.MAGENTA + "Test Results:")
        for idx, res in enumerate(test_results):
            line = f" Test #{idx+1}\n"
            line += f"  Input:    {res.get('input')!r}\n"
            line += f"  Expected: {res.get('expected')!r}\n"
            if res.get("success"):
                line += f"  Output:   {Fore.GREEN}{res.get('output', '')!r}  ✓ Correct"
            elif "error" in res:
                line += f"  Error:    {Fore.RED}{res['error']}  ✗"
            else:
                line += f"  Output:   {Fore.RED}{res.get('output', '')!r}  ✗ Wrong"
            print(line)
        correct_count = sum(1 for r in test_results if r.get("success"))
        print(Fore.CYAN + f"\nPassed {correct_count}/{len(test_results)} test cases")
        print(Fore.YELLOW + f"Time: {elapsed_time:.2f} seconds")
        print(Fore.BLUE + "="*60 + "\n")

    def add_result(self, exercise, solution_code, test_results, elapsed_time):
        self.all_results.append({
            "exercise": exercise["name"],
            "description": exercise["description"],
            "solution": solution_code,
            "test_results": test_results,
            "elapsed_time": elapsed_time
        })

    def save_summary(self, correct_exercises, total_exercises, total_time):
        summary = {
            "correct_exercises": correct_exercises,
            "total_exercises": total_exercises,
            "total_time": total_time
        }
        to_save = {
            "results": self.all_results,
            "summary": summary
        }
        with open(self.save_file, "w", encoding="utf-8") as f:
            json.dump(to_save, f, indent=2, ensure_ascii=False)
        print(Fore.YELLOW + f"\n[OutputManager] Full details saved in {self.save_file}\n")

    def print_summary(self, correct_exercises, total_exercises, total_time):
        print(Style.BRIGHT + Fore.CYAN + f"\nSummary: {correct_exercises}/{total_exercises} correct exercises")
        print(Fore.CYAN + f"Total time: {total_time:.2f} seconds")

    def pretty_print_startup(self):
        print(Style.BRIGHT + Fore.GREEN + "\n==== Starting LLM Exercise Evaluation ====\n")

    def pretty_print_warning(self, msg):
        print(Fore.YELLOW + f"[Warning] {msg}")

    def pretty_print_error(self, msg):
        print(Fore.RED + f"[Error] {msg}")

    def pretty_print_prompt(self, prompt, name):
        print(Style.BRIGHT + Fore.MAGENTA + f"\nPrompt for: {name}\n" + Style.RESET_ALL)
        print(Fore.WHITE + prompt)

    def pretty_print_response(self, response, name):
        print(Style.BRIGHT + Fore.LIGHTBLUE_EX + f"\nResponse for: {name}\n" + Style.RESET_ALL)
        print(Fore.WHITE + str(response))
