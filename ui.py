import os
import chainlit as cl
from chat_agent import ChatAgent
from code_executor import CodeExecutor


@cl.on_chat_start
async def start_chat():
    actions = [
        cl.Action(
            name="model_selection_button",
            icon="mouse-pointer-click",
            payload={"value": "openai"},
            label="OpenAI",
        ),
        cl.Action(
            name="model_selection_button",
            icon="mouse-pointer-click",
            payload={"value": "huggingface"},
            label="HuggingFace",
        ),
    ]

    cl.user_session.set("chat_agent", ChatAgent())
    cl.user_session.set("code_executor", CodeExecutor())
    cl.user_session.set("file_paths", [])

    await cl.Message(
        content="Please select the Model you want to use for the chat.", actions=actions
    ).send()


@cl.action_callback("model_selection_button")
async def on_action(action: cl.Action):
    payload = action.payload
    cl.user_session.set("model_type", payload["value"])
    chat_agent = cl.user_session.get("chat_agent")
    chat_agent.select_model(payload["value"])
    await cl.Message(f"Selected model : {action.label}").send()


@cl.on_message
async def main(message: cl.Message):
    if cl.user_session.get("model_type") is None:
        await cl.Message("Please choose a model once.").send()
        return

    files = []
    uploaded_files = list(filter(lambda x: type(x) is cl.File, message.elements))
    if uploaded_files:
        await handle_upload(uploaded_files)
    if cl.user_session.get("file_paths"):
        files = cl.user_session.get("file_paths")

    chat_agent = cl.user_session.get("chat_agent")
    code_executor = cl.user_session.get("code_executor")

    response = chat_agent.chat(message.content, files=files)
    await cl.Message(content=response).send()

    # Try to extract and execute code
    code_prefix = "```python\n"
    code_suffix = "```"
    if code_prefix in response and code_suffix in response:
        start_index = response.find(code_prefix) + len(code_prefix)
        end_index = response.find(code_suffix, start_index)
        code = response[start_index:end_index].strip()
        execution_result = code_executor.execute_code(code)
        await cl.Message(
            content=f"Code Execution Result: \n```\n{execution_result}\n```"
        ).send()


async def handle_upload(files):
    file_paths = []
    for file in files:
        file_paths.append(file.path)
    cl.user_session.set("file_paths", file_paths)
    await cl.Message(content=f"Uploaded {len(files)} file(s).").send()
