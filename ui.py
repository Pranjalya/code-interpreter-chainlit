
import chainlit as cl
from chat_agent import ChatAgent
from code_executor import CodeExecutor
from utils import save_uploaded_file
import os

chat_agent = ChatAgent()
code_executor = CodeExecutor()


@cl.on_chat_start
async def start_chat():
   cl.user_session.set('file_paths', [])

@cl.on_message
async def main(message: cl.Message):
    files = []
    
    if cl.user_session.get('file_paths'):
        files = cl.user_session.get('file_paths')

    response = chat_agent.chat(message.content, files=files)
    await cl.Message(content=response).send()

    # Try to extract and execute code
    code_prefix = "```python\n"
    code_suffix = "```"
    if code_prefix in response and code_suffix in response:
        start_index = response.find(code_prefix) + len(code_prefix)
        end_index = response.find(code_suffix, start_index)
        code = response[start_index:end_index].strip()
        execution_result = code_executor.execute_code(code, files=files)
        await cl.Message(content=f"Code Execution Result: \n```\n{execution_result}\n```").send()


async def handle_upload(files):
    file_paths = []
    for file in files:
        file_path = save_uploaded_file(file)
        file_paths.append(file_path)
    cl.user_session.set('file_paths', file_paths)
    await cl.Message(content=f"Uploaded {len(files)} file(s).").send()
