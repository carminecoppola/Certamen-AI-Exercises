# AIED

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
git clone https://github.com/your-username/your-repository.git
cd your-repository
```

### 2. **Create and activate a virtual environment**

On **Mac/Linux**:
```sh
python -m venv .venv
source .venv/bin/activate
```

On **Windows**:
```sh
python -m venv .venv
.venv\Scripts\activate
```

### 3. **Install dependencies**

```sh
pip install -r requirements.txt
```

---

## Create the `.env` file

The `.env` file must contain the required API keys. Create it in the project's root directory and add these lines:

```
OPENAI_API_KEY=<your-api-key>
OPENROUTER_API_KEY=<your-api-key>
```

**IMPORTANT:** Never share this file! Ensure `.gitignore` includes `.env` to prevent committing it to GitHub.

---

## Run the Project

After completing the configuration, run the program with:

```sh
python main.py
```

