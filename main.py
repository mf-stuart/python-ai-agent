from google import genai
from google.genai import types

import os
import sys
from dotenv import load_dotenv
from call_function import call_function, available_functions
from system_prompt import system_prompt

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    verbose_flag = "--verbose" in sys.argv

    prompt = " ".join([arg for arg in sys.argv[1:] if not arg.startswith("--")])
    if not prompt:
        print("AI Code Assistant")
        print('\nUsage: python main.py <your-prompt-here> [--verbose]')
        sys.exit(1)

    if verbose_flag:
        print(f"\nUser prompt: {prompt}")

    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]
    generate_response(client, messages, verbose_flag)


def generate_response(client, messages, verbose_flag):

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        )
    )

    if verbose_flag:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    try:
        function_result = call_function(response.function_calls[0], verbose_flag)
        if verbose_flag:
            print(f"-> {function_result.parts[0].function_response.response}")
    except Exception as e:
        raise Exception(f"fatal error: {e}")

def generate_solution(client, messages, verbose_flag):
    pass


if __name__ == "__main__":
    main()