import json
import re

def extract_solution_code(response_content, language="python"):
    """Tries to extract the 'solution' code from the LLM response."""
    try:
        parsed = json.loads(response_content)
        if isinstance(parsed, dict) and "solution" in parsed:
            return {"solution": parsed["solution"]}
    except Exception:
        pass

    match = re.search(r'"solution"\s*:\s*"([\s\S]*?)"\s*[\}\n]', response_content)
    if match:
        sol = match.group(1)
        sol = sol.encode('utf-8').decode('unicode_escape')
        return {"solution": sol}

    match = re.search(r"def solution\(.*?\):[\s\S]+?(?=\n\S|\Z)", response_content)
    if match:
        return {"solution": match.group(0)}

    match = re.search(rf"```{language}\n(.*?)\n```", response_content, re.DOTALL)
    if match:
        return {"solution": match.group(1).strip()}
    return None

def clean_and_parse_json(content_str, language="python"):
    match = re.search(r"```json\n(.*?)\n```", content_str, re.DOTALL)
    if match:
        cleaned_str = match.group(1).strip()
    else:
        match = re.search(rf"```{language}\n(.*?)\n```", content_str, re.DOTALL)
        if match:
            return {"solution": match.group(1).strip()}
        return None
    try:
        return json.loads(cleaned_str)
    except json.JSONDecodeError:
        match = re.search(rf"```{language}\n(.*?)\n```", content_str, re.DOTALL)
        if match:
            return {"solution": match.group(1).strip()}
        return None
