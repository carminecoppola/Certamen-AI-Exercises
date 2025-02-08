from config import Config
from llm_generator import LLMGenerator
from llm_executor import LLMExecutor
from code_evaluator import CodeExecutionFactory

import json
import re


class Main:
    @staticmethod
    def clean_and_parse_json(content_str):
        cleaned_str = re.sub(r"^```json\n|\n```$", "", content_str.strip())
        try:
            return json.loads(cleaned_str)
        except json.JSONDecodeError:
            return None

    @staticmethod
    def run():
        print("Starting program")

        # Initialize LLM Generator
        generator = LLMGenerator(Config.GENERATOR_API_URL, Config.GENERATOR_API_KEY, Config.GENERATOR_MODEL)
        # Initialize LLM Executor
        executor = LLMExecutor(Config.EXECUTOR_API_URL, Config.EXECUTOR_API_KEY, Config.EXECUTOR_MODEL, language="javascript")
        
        # Step 1: Generate exercises with LLM
        exercises = generator.generate_exercises()
        
        # Step 2: Create prompts for LLM
        for exercise in exercises:
            prompt = executor.create_prompt(exercise)
            if not prompt:
                print("No valid exercise!")
                continue
            print(prompt)
            
            # print(exercise)
            print(f"Requesting solution for: {exercise['name']}\n")

            # Step 3: Generate solution for each exercise with LLM
            response_data = executor.query_model(prompt)
            content = Main.clean_and_parse_json(response_data)
            if content and "solution" in content:
                code = content["solution"]

                # Step 4: Evaluate LLM solution code
                results = CodeExecutionFactory.get_executor(executor.language, code,  exercise["input"], exercise["output"])
                print("Test Results:", results)
                correct_count = sum(1 for result in results if result.get("success", False))
                print(f"Number of correct test cases: {correct_count}/{len(exercise['input'])}")
            else:
                print("Error: No valid solution received from LLM.")
                continue

            # TODO: remove it (just for testing)
            break


if __name__ == "__main__":
    Main.run()
