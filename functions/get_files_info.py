from google.genai import types

import os

def get_files_info(working_directory, directory=None):
    cwd_path = os.path.abspath(working_directory)
    if directory:
        full_path = os.path.join(cwd_path, directory)
    else:
        full_path = cwd_path

    if not os.path.exists(cwd_path) and directory != "." and directory not in os.listdir(cwd_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    try:
        files = os.listdir(full_path)
        files.sort()
        return_strings = []
        for fn in files:
            fn_path = os.path.join(full_path, fn)
            return_strings.append(f"- {fn}: file_size={os.path.getsize(fn_path)} bytes, is_dir={os.path.isdir(fn_path)}")
        return "\n".join(return_strings) + "\n"

    except FileNotFoundError:
       return f'Error: "{working_directory}" is not a directory'
    except PermissionError:
        return f'Error: "{working_directory}" cannot be accessed'

schema_get_files_info = types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                ),
            },
        ),
    )
