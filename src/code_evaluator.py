from pythonmonkey import eval as js_eval
import tempfile
import json
import subprocess
import os
import re


class CodeExecutor:
    """Base class for executing code in different programming languages."""
    def __init__(self, code, test_inputs, expected_outputs):
        self.code = code
        self.test_inputs = test_inputs
        self.expected_outputs = expected_outputs
        self.results = []

    def execute(self):
        """To be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement execute method.")

    def execute_function(self, func):
        """Executes the function and compares output with expected values."""

        for test_input, expected_output in zip(self.test_inputs, self.expected_outputs):
            try:
                if isinstance(test_input, (list, tuple)):
                    output = func(*test_input)
                else:
                    output = func(test_input)

                if self.language == "Java":
                    expected_output_tmp = str(expected_output)
                    if isinstance(expected_output, bool):
                        expected_output_tmp = str(expected_output).lower()

                    expected_output = expected_output_tmp

                self.results.append({
                    "input": test_input,
                    "expected": expected_output,
                    "output": output,
                    "success": output == expected_output
                })
            except Exception as e:
                self.results.append({
                    "input": test_input,
                    "error": str(e),
                    "success": False
                })

        return self.results


class PythonExecutor(CodeExecutor):
    """Executes Python code dynamically using exec()."""
    def __init__(self, code, test_inputs, expected_outputs):
        super().__init__(code, test_inputs, expected_outputs)
        self.language = "Python"

    def execute(self):
        global_scope = {}
        try:
            exec(self.code, global_scope)
            function_name = [name for name in global_scope if callable(global_scope[name])][0]
            return self.execute_function(global_scope[function_name])
        except Exception as e:
            return [{"error": f"Python execution failed: {str(e)}", "success": False}]


class JavaScriptExecutor(CodeExecutor):
    """Executes JavaScript code using PythonMonkey."""
    def __init__(self, code, test_inputs, expected_outputs):
        super().__init__(code, test_inputs, expected_outputs)
        self.language = "JavaScript"

    def execute(self):
        try:
            js_eval(self.code)
            function_name = self.code.split("function ")[1].split("(")[0].strip()
            return self.execute_function(lambda *args: js_eval(f"{function_name}({','.join(map(json.dumps, args))})"))
        except Exception as e:
            return [{"error": f"JavaScript execution failed: {str(e)}", "success": False}]


class JavaExecutor(CodeExecutor):
    """Executes Java code by compiling and running it as a subprocess."""
    def __init__(self, code, test_inputs, expected_outputs):
        super().__init__(code, test_inputs, expected_outputs)
        self.language = "Java"

    def execute(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            java_file_path = os.path.join(temp_dir, "Solution.java")
            class_file_path = os.path.join(temp_dir, "Solution.class")

            with open(java_file_path, "w") as f:
                f.write(self.code)

            try:
                subprocess.run(["javac", java_file_path], check=True, cwd=temp_dir)

                class_name_match = re.search(r"public\s+class\s+(\w+)", self.code)
                class_name = class_name_match.group(1) if class_name_match else "Solution"

                def run_java_program(*input_values):
                    cmd = ["java", "-cp", temp_dir, class_name] + [str(e) for e in input_values]
                    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                    return result.stdout.strip()
                    
                    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                    return result.stdout.strip()

                return self.execute_function(run_java_program)

            except subprocess.CalledProcessError as e:
                return [{"error": f"Java execution failed: {str(e)}", "success": False}]


class CodeExecutionFactory:
    """Factory to create the appropriate executor based on language."""
    EXECUTOR_CLASSES = {
        "python": PythonExecutor,
        "javascript": JavaScriptExecutor,
        "java": JavaExecutor
    }

    @staticmethod
    def get_executor(language, code, test_inputs, expected_outputs):
        executor_class = CodeExecutionFactory.EXECUTOR_CLASSES.get(language.lower())
        if not executor_class:
            return [{"error": f"Unsupported language: {language}", "success": False}]
        return executor_class(code, test_inputs, expected_outputs).execute()
