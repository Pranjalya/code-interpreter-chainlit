
from openai import OpenAI

client = OpenAI(api_key=self.api_key)
from utils import load_env_variables

class ChatAgent:
    def __init__(self):
        self.api_key = load_env_variables()
        self.chat_history = []
        self.model_name = "gpt-3.5-turbo"

    def _create_prompt(self, user_message, files=None):
        """Constructs the prompt for the OpenAI API."""
        prompt = []
        if files:
            for file in files:
                prompt.append(f"User uploaded the file: {file}")
        prompt.append(f"User: {user_message}")
        return "\n".join(prompt)

    def chat(self, user_message, files=None):
        """Sends the prompt to the OpenAI API and returns the response."""
        prompt = self._create_prompt(user_message, files)
        self.chat_history.append({"role": "user", "content": prompt})
        response = client.chat.completions.create(model=self.model_name, messages=self.chat_history)
        assistant_response = response.choices[0].message.content
        self.chat_history.append({"role":"assistant", "content": assistant_response})
        return assistant_response
