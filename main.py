from src.config import Config
from src.llm_generator import LLMGenerator
from src.llm_executor import LLMExecutor
from src.code_evaluator import CodeExecutionFactory
from src.output_manager import OutputManager
from src.utils import extract_solution_code

import argparse
import time

class Main:
    @staticmethod
    def parse_arguments():
        parser = argparse.ArgumentParser(description="Run LLM exercise generator and evaluator.")
        parser.add_argument("--language", type=str, choices=["python", "javascript", "java"], default="python",
                            help="Programming language for exercises (default: python)")
        return parser.parse_args()

    @staticmethod
    def run():
        args = Main.parse_arguments()
        language = args.language

        output_manager = OutputManager()
        output_manager.pretty_print_startup()

        generator = LLMGenerator(Config.GENERATOR_API_URL, Config.GENERATOR_API_KEY, Config.GENERATOR_MODEL)
        executor = LLMExecutor(Config.EXECUTOR_API_URL, Config.EXECUTOR_API_KEY, Config.EXECUTOR_MODEL,
                               language=language)

        exercises = generator.generate_exercises()
        total_exercises = len(exercises)
        correct_exercises = 0
        total_start_time = time.time()

        for exercise in exercises:
            start_time = time.time()
            prompt = executor.create_prompt(exercise)
            if not prompt:
                output_manager.pretty_print_warning("No valid exercise!")
                continue

            output_manager.pretty_print_prompt(prompt, exercise["name"])
            response_data = executor.query_model(prompt)
            content = extract_solution_code(response_data, language)
            output_manager.pretty_print_response(content, exercise["name"])

            if content and "solution" in content:
                code = content["solution"]
                results = CodeExecutionFactory.get_executor(
                    executor.language, code, exercise["input"], exercise["output"]
                )
                correct_count = sum(1 for result in results if result.get("success", False))
                end_time = time.time()
                elapsed_time = end_time - start_time

                output_manager.pretty_print_result(exercise, code, results, elapsed_time)
                output_manager.add_result(exercise, code, results, elapsed_time)

                if correct_count == len(exercise["input"]):
                    correct_exercises += 1
            else:
                output_manager.pretty_print_error("No valid solution received from LLM.")
                continue

        total_end_time = time.time()
        total_elapsed_time = total_end_time - total_start_time
        output_manager.print_summary(correct_exercises, total_exercises, total_elapsed_time)
        output_manager.save_summary(correct_exercises, total_exercises, total_elapsed_time)

if __name__ == "__main__":
    Main.run()
