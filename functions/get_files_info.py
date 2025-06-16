import os

def get_files_info(working_directory, directory=None):
    cwd_path = os.path.abspath(working_directory)
    full_path = os.path.join(cwd_path, directory)

    if not os.path.exists(cwd_path) or directory not in os.listdir(cwd_path):
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
