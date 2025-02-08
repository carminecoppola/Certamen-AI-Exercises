import json

def execute_python_code(code, test_inputs, expected_outputs):
    results = []
    local_scope = {}

    try:
        exec(code, {}, local_scope)

        function_name = list(local_scope.keys())[0]
        function = local_scope[function_name]

        for test_input, expected_output in zip(test_inputs, expected_outputs):
            try:
                output = function(test_input)
                results.append({
                    "input": test_input,
                    "expected": expected_output,
                    "output": output,
                    "success": output == expected_output
                })
            except Exception as e:
                results.append({
                    "input": test_input,
                    "error": str(e),
                    "success": False
                })
    except Exception as e:
        return [{"error": f"Code execution failed: {str(e)}", "success": False}]

    return results
