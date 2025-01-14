
import io
import contextlib
import traceback
import os

class CodeExecutor:
    def __init__(self):
        self.namespace = {}

    def execute_code(self, code, files=None):
        """Executes the given Python code and returns the output."""
        if files:
            for file in files:
                try:
                    filename = os.path.basename(file)
                    with open(file, 'r') as f:
                        file_content = f.read()
                        self.namespace[filename] = file_content # Add file content to the namespace
                except Exception as e:
                    return f"Error loading file {filename}: {e}"

        output = io.StringIO()
        try:
            with contextlib.redirect_stdout(output):
                exec(code, self.namespace)
            return output.getvalue()
        except Exception as e:
            error_message = f"Error executing code: {e}\n"
            error_message += f"Traceback:\n{traceback.format_exc()}"
            return error_message
