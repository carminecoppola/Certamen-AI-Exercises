# Certamen-AI-Exercises
Certamen-AI-Exercises uses LLMs to automatically generate and evaluate programming exercises, creating a closed-loop iterative learning system.
The goal is to enhance automated learning frameworks and refine AI-based educational tools.

## Requirements

Before starting, make sure you have installed:

- Python **3.10+**
- An account on **OpenAI** and **OpenRouter** with active API keys
- `pip` and `venv` for virtual environment management

---

## Configuration

### 1. **Clone the repository**

Open a terminal and clone the project:

```sh
https://github.com/carminecoppola/Certamen-AI-Exercises.git
cd Certamen-AI-Exercises
```

### 2. **Create and activate a virtual environment**

On **Mac/Linux**:
```sh
python -m venv .venv
source .venv/bin/activate
```


### 3. **Install dependencies**

```sh
pip install -r requirements.txt
```

---

## Create the `.env` file

The `.env` file must contain the required API keys. Create it in the project's root directory and add these lines:

```
GENERATOR_API_KEY=<your-api-key>
GENERATOR_API_URL=https://api.openai.com/v1/
GENERATOR_MODEL=gpt-4

EXECUTOR_API_KEY=<your-api-key>
EXECUTOR_API_URL=https://openrouter.ai/api/v1/
EXECUTOR_MODEL=deepseek/deepseek-r1:free
```

**IMPORTANT:** Never share this file! Ensure `.gitignore` includes `.env` to prevent committing it to GitHub.

---

## Run the Project

After completing the configuration, run the program with:

```sh
python main.py
```
---

## Demo


https://github.com/user-attachments/assets/2fa5abe2-f241-4891-af86-fa88a8a490bb


