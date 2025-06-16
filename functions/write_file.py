import os

def write_file(working_directory, file_path, content):
    try:
        cwd_path =  os.path.abspath(os.path.join(working_directory, *file_path.split(os.sep)[:-1]))
        file_name = os.path.basename(file_path)
        full_path = os.path.join(cwd_path, file_name)

        if not os.path.exists(cwd_path) or not os.path.normpath(cwd_path).startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot read "{file_name}" as it is outside the permitted working directory'

        with open(full_path, "w") as file:
            file.write(content)
        return f'Successfully wrote to "{file_name}" ({len(content)} characters written)'

    except FileNotFoundError:
        return f'Error: File not found or is not a regular file: "{file_name}"'
    except PermissionError:
        return f'Error: "{working_directory}" cannot be accessed'
    except IOError:
        return f'Error: "{working_directory}" cannot be accessed'