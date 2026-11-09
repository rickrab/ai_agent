import os
import sys
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions
import json
from call_function import call_function


#=================================================================================#

def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key == None:
        raise RuntimeError("API key empty or not found")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]


    for _ in range(20):

        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            temperature=0,
            tools=available_functions,
        )

        usage = response.usage
        message = response.choices[0].message
        messages.append(message)

        if args.verbose == True:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {usage.prompt_tokens}")
            print(f"Response tokens: {usage.completion_tokens}")
            print("Response:")

        if message.tool_calls != None:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call, args.verbose)
                if result_message["content"] == None:
                    raise ValueError("Missing required content in result_message.")
                if args.verbose == True:
                    print(f"-> {result_message['content']}")
                messages.append(result_message)

        if message.tool_calls == None:
            print(response.choices[0].message.content)
            break
        if _ >= 20:
            print("Maximum number of iterations exceeded")
            sys.exit(1)



#=================================================================================#

if __name__ == "__main__":
    main()
