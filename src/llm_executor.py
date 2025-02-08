import json
import openai
from config import Config

class LLMExecutor:
    def __init__(self, api_url, api_key, model):
        self.api_key = api_key
        self.model = model
        self.client = openai.OpenAI(base_url=api_url, api_key=api_key)

    def create_prompt(self, data) -> str:
        """Reads an input exercise and generates a prompt."""
        if data and "name" in data and "description" in data:
            return f"""
                Return a Python function that takes a single argument and produces an output based on the given description.

                Exercise: {data['name']}
                Description: {data['description']}

                The response must be in a valid JSON format:
                {{
                    "exercise": "{data['name']}",
                    "solution": "def solution(input_value):\\n    # Implement the function here\\n    return result",
                    "input": {json.dumps(data.get('input', []))},
                    "output": {json.dumps(data.get('output', []))}
                }}
                """
        return ""

    def query_model(self, prompt):
        """Sends a request to OpenAI's API and returns the response."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content.strip()
        except openai.OpenAIError as e:
            print(f"OpenAI API error: {e}")
            return None
