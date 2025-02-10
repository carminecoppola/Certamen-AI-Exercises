import json
import openai
import os
from src.config import Config


class LLMExecutor:
    def __init__(self, api_url, api_key, model, language="python", debug=False):
        self.api_key = api_key
        self.model = model
        self.client = openai.OpenAI(base_url=api_url, api_key=api_key)
        self.language = language
        self.debug = debug  # Controlla se stampare log dettagliati

    def create_prompt(self, data) -> str:
        """Generating a prompt for the LLM with the given data."""
        if data and "name" in data and "description" in data:
            return f"""
            Return a {self.language} function that takes a single argument and produces an output based on the given description.

            Exercise: {data['name']}
            Description: {data['description']}

            The response must be in a valid JSON format:
            {{
                "exercise": "{data['name']}",
                "solution": {json.dumps(self.generate_function_template())},
                "input": {json.dumps(data.get('input', []))},
                "output": {json.dumps(data.get('output', []))}
            }}
            """
        return ""

    def query_model(self, prompt, save_response=True):
        """Send the request to the LLM and return the response."""
        try:
            if self.debug:
                print(f"[DEBUG] Sending request to LLM ({self.model})...")

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )

            # Valid response control
            if not response or not hasattr(response, "choices") or not response.choices:
                print("Error: LLM response is empty or invalid.")
                return None

            response_content = response.choices[0].message.content.strip()

            # Log of the response only if the value of debug is TRUE
            if self.debug:
                print(f"[DEBUG] LLM Response: {response_content}")

            # Saving the response only if it's required
            if save_response:
                self.save_response_to_json(prompt, response_content)

            return response_content

        except openai.OpenAIError as e:
            print(f"OpenAI API error: {e}")
            return None

    def save_response_to_json(self, prompt, response_content):
        """Save the response of the LLM in a JSON file for each language."""
        filename = f"executor_responses_{self.language}.json"
        response_data = {
            "prompt": prompt.strip(),
            "response": response_content
        }

        # If the file already exists, search for the existing data
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                try:
                    existing_data = json.load(f)
                except json.JSONDecodeError:
                    existing_data = []  # Se il file è corrotto, iniziamo da zero
        else:
            existing_data = []

        # Adding the new response
        existing_data.append(response_data)

        # Limit the number of saved responses to 10
        if len(existing_data) > 10:
            existing_data = existing_data[-10:]

        # Write the updated data in the JSON file
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, indent=4, ensure_ascii=False)

        if self.debug:
            print(f"[DEBUG] Executor response saved in {filename}")

    def generate_function_template(self):
        """Generates a function template for the selected programming language."""
        templates = {
            "python": """def solution(input_value):\n\n\t# Implement the function logic here\n\n\treturn result""",
            "javascript": """function solution(inputValue) {\n\n\t// Implement the function logic here\n\n\treturn result;\n}""",
            "c": """#include <stdio.h>\n\nint solution(int input) {\n    // Implement the function logic here\n    return 0;\n}\n\nint main() {\n    int input;\n    scanf("%d", &input);\n    printf("%d\\n", solution(input));\n    return 0;\n}""",
            "cpp": """#include <iostream>\nusing namespace std;\n\nint solution(int input) {\n    // Implement the function logic here\n    return 0;\n}\n\nint main() {\n    int input;\n    cin >> input;\n    cout << solution(input) << endl;\n    return 0;\n}"""
        }
        return templates.get(self.language, "// Unsupported language")
