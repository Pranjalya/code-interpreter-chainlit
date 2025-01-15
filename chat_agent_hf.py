
import pandas as pd
from huggingface_hub import InferenceClient
from utils import load_env_variables

SYSTEM_PROMPT = f"""You are an expert coding assistant and interpreter.
You will receive code instructions and path to the files which are present locally in correct path. 
You need to generate Python code based on the instructions and using the local file paths given, execute the code and return the result in the manner it was asked.
You may not be able to read the files, but the code execution process will be able to.
If any libraries are required, first run `pip install <library 1> <library 2>` to install the dependencies.
"""

class ChatAgent:
    def __init__(self):
        self.api_key = load_env_variables("huggingface")
        self.client = InferenceClient(api_key=self.api_key)
        self.chat_history = [{"role": "system", "content": SYSTEM_PROMPT}]
        self.model_name = "Qwen/Qwen2.5-Coder-32B-Instruct"

    def _create_prompt(self, user_message, files=None):
        """Constructs the prompt for the Hugging Face model, including file samples."""
        prompt = []
        if files:
            for file in files:
                try:
                    df = pd.read_csv(file)
                    sample = df.head(2).to_string() # Taking head of the file to avoid adding too much context
                    prompt.append(f"User uploaded file: {file}, Sample data:\n{sample}\n")
                except Exception as e:
                    prompt.append(f"User uploaded file: {file}, but there was error in reading the file: {e}")
        prompt.append(f"NOTE: While generating the code, do not try to execute it and do not return the output on the sample data.")
        prompt.append(f"User: {user_message}")
        return "\n".join(prompt)

    def chat(self, user_message, files=None):
        """Sends the prompt to the OpenAI API and returns the response."""
        prompt = self._create_prompt(user_message, files)
        self.chat_history.append({"role": "user", "content": prompt})
        response = self.client.chat.completions.create(model=self.model_name, messages=self.chat_history)
        assistant_response = response.choices[0].message.content
        self.chat_history.append({"role":"assistant", "content": assistant_response})
        return assistant_response
