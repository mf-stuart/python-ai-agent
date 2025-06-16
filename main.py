import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions import *
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python import run_python_file
from functions.write_file import write_file


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    verbose_flag = False

    try:
        prompt = sys.argv[1]
    except IndexError:
        exit(code=1)

    try:
        if sys.argv[2] == "--verbose":
            verbose_flag = True
    except IndexError:
        pass


    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]


    generate_response(client, prompt, messages, verbose_flag)

def call_function(function_call_part, verbose_flag=False):
    WORKING_DIRECTORY = "./calculator"
    func_dict = {
        "run_python_file": run_python_file,
        "write_file": write_file,
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
    }


    if verbose_flag:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    try:
        result = func_dict[function_call_part.name](WORKING_DIRECTORY, **function_call_part.args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": result},
                )
            ],
        )
    except KeyError:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

def generate_response(client, prompt, messages, verbose_flag):
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

    schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description="Writes the specified file to the specified directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The file to write, relative to the current working directory."),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="The content to write, as a string."
                ),
            },
        ),
    )


    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

    system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories
        - Read file contents
        - Execute python files with optional arguments
        - Write or overwrite files

        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

        """

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        )
    )

    if verbose_flag:
        print(f"\nUser prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    try:
        function_result = call_function(response.function_calls[0], verbose_flag)
        if verbose_flag:
            print(f"-> {function_result.parts[0].function_response.response}")
    except Exception as e:
        raise Exception(f"fatal error: {e}")


if __name__ == "__main__":
    main()