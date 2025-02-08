import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    GENERATOR_API_KEY = os.getenv("GENERATOR_API_KEY")
    GENERATOR_API_URL = os.getenv("GENERATOR_API_URL")
    GENERATOR_MODEL = os.getenv("GENERATOR_MODEL")

    EXECUTOR_API_KEY = os.getenv("EXECUTOR_API_KEY")
    EXECUTOR_API_URL = os.getenv("EXECUTOR_API_URL")
    EXECUTOR_MODEL = os.getenv("EXECUTOR_MODEL")
