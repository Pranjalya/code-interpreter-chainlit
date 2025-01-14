
import os
from dotenv import load_dotenv

def load_env_variables():
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables.")
    return openai_api_key

def save_uploaded_file(file, directory='/app/input_files'):
    """Save an uploaded file to a specific directory."""
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, file.filename)
    with open(file_path, 'wb') as f:
        f.write(file.content)
    return file_path
