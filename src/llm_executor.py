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
        self.debug = debug  # Check whether to print detailed logs.

    def create_prompt(self, data) -> str:
        """Generating a prompt for the LLM with the given data."""
        if data and "name" in data and "description" in data:
            return f"""
            Return a {self.language} code that MUST take as input some parameters and MUST produces an output based on the given description. 
            The function MUST return only the result, without any string. 
            If the exercise has more than one argument, ensure that all parameters are correctly handled and passed to the function.
            The function should accept multiple inputs separately and process them accordingly.
            If the language is Java, add also the main and read the parameters from args.


            Exercise: {data['name']}
            Description: {data['description']}


            The response must be in a valid JSON format:
            {{
                "exercise": "{data['name']}",
                "solution": {json.dumps(self.generate_function_template())}
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

            # Verify that the answer is valid
            if not response or not hasattr(response, "choices") or not response.choices:
                print("Error: LLM response is empty or invalid.")
                return None

            response_content = response.choices[0].message.content.strip()

            # Response log only if debug is active
            if self.debug:
                print(f"[DEBUG] LLM Response: {response_content}")

            # Save response only if required
            if save_response:
                self.save_response_to_json(prompt, response_content)

            return response_content

        except openai.OpenAIError as e:
            print(f"OpenAI API error: {e}")
            return None

    def save_response_to_json(self, prompt, response_content):
        """Save the response of the LLM in a JSON file for each language."""
        filename = f"executor_responses_{self.language}.json"
        print(f"")
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
                    existing_data = []  # If the file is corrupt, we start from scratch.
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
