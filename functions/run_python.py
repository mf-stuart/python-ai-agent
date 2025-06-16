from google.genai import types

import os
import subprocess

def run_python_file(working_directory, file_path):
    try:
        print("\n")
        cwd_path =  os.path.abspath(os.path.join(working_directory, *file_path.split(os.sep)[:-1]))
        file_name = os.path.basename(file_path)
        full_path = os.path.join(cwd_path, file_name)

        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'

        if not os.path.normpath(cwd_path).startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(full_path):
            return f'Error: File "{file_name}" not found'

        process_result = subprocess.run(["python", full_path], cwd=cwd_path, timeout=30, capture_output=True)

        output_elts = []
        if process_result.stdout.strip():
            output_elts.append(f"STDOUT:{process_result.stdout}")
        else:
            output_elts.append("No output produced.")
        if process_result.stderr.strip():
            output_elts.append(f"STDERR:{process_result.stderr}")
        if process_result.returncode != 0:
            output_elts.append(f"Process exited with code {process_result.returncode}")
        return "\n".join(output_elts)
    except FileNotFoundError:
        return f'Error: File "{file_name}" not found'
    except PermissionError:
        return f'Error: "{working_directory}" cannot be accessed'
    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the specified python file from the specified directory and returns a string of it's result, including stdout and stderr.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to execute, relative to the current working directory."
            ),
        },
    ),
)