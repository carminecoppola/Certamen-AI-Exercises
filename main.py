from src.config import Config
from src.llm_generator import LLMGenerator
from src.llm_executor import LLMExecutor
from src.code_evaluator import CodeExecutionFactory

import argparse
import json
import re
import time


class Main:
    @staticmethod
    def parse_arguments():
        """Parses command-line arguments."""
        parser = argparse.ArgumentParser(description="Run LLM exercise generator and evaluator.")
        parser.add_argument("--language", type=str, choices=["python", "javascript"], default="python",
                            help="Programming language for exercises (default: python)")
        return parser.parse_args()

    @staticmethod
    def clean_and_parse_json(content_str, language) :
        cleaned_str = re.sub(r"^```json\n|\n```$", "", content_str.strip())

        try :
            return json.loads(cleaned_str)
        except json.JSONDecodeError :
            match = re.search(rf'```{language}\n(.*?)\n```', content_str, re.DOTALL)
            print("\nProblem of response, parse the json file")
            if match :
                return {"solution" : match.group(1).strip()}
            return None


    @staticmethod
    def run():
        args = Main.parse_arguments()
        language = args.language

        print("Starting program")

        # Initialize LLM Generator
        generator = LLMGenerator(Config.GENERATOR_API_URL, Config.GENERATOR_API_KEY, Config.GENERATOR_MODEL)
        # Initialize LLM Executor
        executor = LLMExecutor(Config.EXECUTOR_API_URL, Config.EXECUTOR_API_KEY, Config.EXECUTOR_MODEL,
                               language=language)

        # Step 1: Generate exercises with LLM
        exercises = generator.generate_exercises()
        total_exercises = len(exercises)
        correct_exercises = 0

        # Track total time
        total_start_time = time.time()

        # Step 2: Create prompts for LLM
        for exercise in exercises:
            start_time = time.time()
            prompt = executor.create_prompt(exercise)
            if not prompt:
                print("No valid exercise!")
                continue
            print("Prompt: ",prompt)

            print(f"Requesting solution for: {exercise['name']}\n")

            # Step 3: Generate solution for each exercise with LLM
            response_data = executor.query_model(prompt)
            content = Main.clean_and_parse_json(response_data, language)
            print(f"Response: {content}")
            if content and "solution" in content:
                code = content["solution"]

                # Step 4: Evaluate LLM solution code
                results = CodeExecutionFactory.get_executor(executor.language, code, exercise["input"],
                                                            exercise["output"])
                print("Test Results:", results)
                correct_count = sum(1 for result in results if result.get("success", False))
                print(f"Number of correct test cases: {correct_count}/{len(exercise['input'])}")

                if correct_count == len(exercise["input"]):
                    correct_exercises += 1
            else:
                print("Error: No valid solution received from LLM.")
                continue


            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Time taken for {exercise['name']}: {elapsed_time:.2f} seconds\n")


        total_end_time = time.time()
        total_elapsed_time = total_end_time - total_start_time

        print(f"\nSummary: Correct exercises {correct_exercises}/{total_exercises}")
        print(f"\nTotal time: {total_elapsed_time:.2f} seconds\n")


if __name__ == "__main__":
    Main.run()
