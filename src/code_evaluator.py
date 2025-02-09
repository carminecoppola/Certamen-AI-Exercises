from pythonmonkey import eval as js_eval
import json


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
                output = func(test_input)
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

    def execute(self):
        try:
            js_eval(self.code)
            function_name = self.code.split("function ")[1].split("(")[0].strip()
            return self.execute_function(lambda x: js_eval(f"{function_name}({json.dumps(x)})"))
        except Exception as e:
            return [{"error": f"JavaScript execution failed: {str(e)}", "success": False}]


class CodeExecutionFactory:
    """Factory to create the appropriate executor based on language."""
    
    EXECUTOR_CLASSES = {
        "python": PythonExecutor,
        "javascript": JavaScriptExecutor
    }

    @staticmethod
    def get_executor(language, code, test_inputs, expected_outputs):
        executor_class = CodeExecutionFactory.EXECUTOR_CLASSES.get(language.lower())
        if not executor_class:
            return [{"error": f"Unsupported language: {language}", "success": False}]
        return executor_class(code, test_inputs, expected_outputs).execute()
