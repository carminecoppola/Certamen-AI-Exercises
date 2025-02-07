import tempfile
import os
import re
import subprocess
import sys
import io
import inspect

def create_temp_output_file():
    """Crea un file temporaneo per salvare l'output del codice eseguito."""
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8")
    print(f"📄 Output salvato in: {temp_file.name}")
    return temp_file.name  # Restituisce il percorso


def detect_language(code):
    """Identifica il linguaggio di programmazione analizzando la sintassi."""
    if "def " in code and ":" in code:
        return "python"
    elif "function " in code or "console.log(" in code:
        return "javascript"
    elif "public static void main" in code or "class " in code:
        return "java"
    elif "#include <stdio.h>" in code or "int main()" in code:
        return "c"
    elif "#include <iostream>" in code or "std::cout" in code:
        return "cpp"
    else:
        return "unknown"

