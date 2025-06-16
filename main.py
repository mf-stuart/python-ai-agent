import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

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
    response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages)

    printout(prompt, response, messages, verbose_flag)

def printout(prompt, response, messages, verbose_flag):
    if verbose_flag:
        print(f"\nUser prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(f"\n{response.text}")


if __name__ == "__main__":
    main()