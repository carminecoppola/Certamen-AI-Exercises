import json
import json5
import openai
import os
import re
from src.config import Config


class LLMGenerator:
    def __init__(self, api_url, api_key, model, filename="generated_exercises.json"):
        self.api_key = api_key
        self.model = model
        self.client = openai.OpenAI(base_url=api_url, api_key=api_key)
        self.filename = filename

    def generate_exercises(self, force_regenerate=False):
        """Generates a list of programming exercises using OpenAI and saves them in a JSON file."""

        # If the file exists, and we don't want to regenerate, we read the existing data.
        if not force_regenerate and os.path.exists(self.filename):
            print(f"Loading exercises from {self.filename}")
            return self.load_exercises_from_json()

        # Prompt for generating the exercises
        prompt = """
        Generate a list of 10 programming exercises in JSON format. Each exercise must strictly follow this structure:

        [
            {
                "name": "<A concise and clear title for the exercise>",
                "description": "<A detailed description of the exercise, specifying exactly what needs to be implemented>",
                "input": [<A list of example inputs of the correct type that will be used to test the solution>],
                "output": [<A list of expected outputs of the correct type corresponding to each input>]
            }
        ]

        ### Constraints:
        1. Each exercise must explicitly define a **set of input values** in the `"input"` field.
        2. Each exercise must explicitly define the **expected output values** in the `"output"` field.
        3. The **number of elements in `"input"` and `"output"` must always match**, ensuring testability.
        4. **Data types must be correct for both inputs and outputs**:
            - If the function expects **integers**, provide integers in `"input"`, not strings.
            - If the function expects **floating-point numbers**, use decimals (e.g., `3.14`).
            - If the function expects **strings**, provide strings.
            - If the function expects **boolean values**, return actual boolean values (`true/false`), not strings.
            - If the function expects **lists**, provide lists with elements of the correct type.
            - If the function expects **dictionaries (maps)**, provide correctly formatted JSON objects.
        5. Ensure diverse exercises covering different programming concepts such as **loops, recursion, data structures, and algorithms**.
        6. The **JSON output must be properly formatted and valid**.
        """

        try:
            print(f"Generating exercises using {self.model} ...")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": prompt}]
            )

            # Valid response control
            if not response or not hasattr(response, "choices") or not response.choices:
                print("Error: LLM response is empty or invalid.")
                return []

            raw_response = response.choices[0].message.content.strip()
            exercises = self.clean_and_validate_json(raw_response)

            if exercises:
                self.save_exercises_to_json(exercises)  # We save exercises in JSON
                print(f"Exercises saved in {self.filename}")

            return exercises if exercises else []

        except openai.OpenAIError as e:
            print(f"OpenAI API error: {e}")
            return []

    def save_exercises_to_json(self, exercises):
        """Save the exercises in a JSON file."""
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(exercises, f, indent=4, ensure_ascii=False)
            print(f"Exercises successfully saved in {self.filename}")
        except IOError as e:
            print(f"Error saving exercises to file: {e}")

    def load_exercises_from_json(self):
        """Load the exercises from the existing JSON file."""
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading exercises from file: {e}")
            return []

    @staticmethod
    def clean_and_validate_json(response_text):
        """Extracts and validates a JSON from a response."""
        try:
            response_text = response_text.strip("```json").strip("```").strip()
            match = re.search(r"\[.*\]", response_text, re.DOTALL)
            return json.loads(match.group(0)) if match else json5.loads(response_text)
        except json.JSONDecodeError:
            print("Invalid JSON format.")
            return None
