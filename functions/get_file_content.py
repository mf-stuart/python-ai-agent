import os
MAX_CHARACTERS = 10000

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