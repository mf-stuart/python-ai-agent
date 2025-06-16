import os
from google.genai import types
from config import MAX_CHARACTERS

def get_file_content(working_directory, file_path):
    try:
        cwd_path =  os.path.abspath(os.path.join(working_directory, *file_path.split(os.sep)[:-1]))
        file_name = os.path.basename(file_path)
        full_path = os.path.join(cwd_path,file_name)

        if (not os.path.exists(cwd_path)
                or not os.path.normpath(cwd_path).startswith(os.path.abspath(working_directory))
                or file_name not in os.listdir(cwd_path)):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        with open(full_path, "r") as file:
            contents = file.read(MAX_CHARACTERS)
        return (contents + f'[...File "{file_name}" truncated at 10000 characters]' if len(contents) == 10000 else contents) + "\n"
    except FileNotFoundError:
        return f'Error: File not found or is not a regular file: "{file_name}"'
    except PermissionError:
        return f'Error: "{working_directory}" cannot be accessed'

schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
        description="Gets file content from the specified directory and returns a string of it's content. String is truncated to 10000 characters if needed and a message is appended on the end. ",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The file to read from, relative to the current working directory."
                ),
            },
        ),
    )