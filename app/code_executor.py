import io
import contextlib
import traceback
import os


class CodeExecutor:
    def __init__(self):
        pass

    def execute_code(self, code):
        """Executes the given Python code and returns the output."""
        output = io.StringIO()
        try:
            with contextlib.redirect_stdout(output):
                exec(code)
            return output.getvalue()
        except Exception as e:
            error_message = f"Error executing code: {e}\n"
            error_message += f"Traceback:\n{traceback.format_exc()}"
            return error_message
