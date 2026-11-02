import json
import os
from prompts import system_prompt
from dotenv import load_dotenv
from openai import OpenAI
import argparse

from call_functions import available_functions 
from call_functions import call_function



def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("API key not founnd")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    ) 

    parser = argparse.ArgumentParser(description="Input user prompt.")
    parser.add_argument("user_prompt", type = str, help="User prompt")
    parser.add_argument("--verbose", action = "store_true", help="Enable verbose outpput")
    args = parser.parse_args()

    messages=[
        {
            "role": "system",
            "content":system_prompt 
        },
        {
            "role": "user",
            "content": args.user_prompt
        }
    ]

    output = generate_content(client, messages)
    message = output.choices[0].message

    if args.verbose:
        print(f"User prompt: {messages[0]['content']}")
        print(f"Prompt tokens:{output.usage.prompt_tokens}") # type: ignore
        print(f"Response tokens: {output.usage.completion_tokens}") # type: ignore
        print("")
    
    print("Response:")
    print(message.content)
    print("")

    # print(message.tool_calls) # Example: [ChatCompletionMessageFunctionToolCall(id='call-76eff4e8-cf09-49d3-a697-f68a9584801f', function=Function(arguments='{"file_path":"main.txt","content":"hello"}', name='write_file'), type='function', index=0)]
    if message.tool_calls:
        for tool_call in message.tool_calls:
            # function_args = json.loads(tool_call.function.arguments or "{}") # type: ignore
            # print(f"Calling function: {tool_call.function.name}({function_args})") # type: ignore
            
            result_message = call_function(tool_call)
            
            if not result_message['content']:
                raise Exception("Empty function content")
            if args.verbose:
                print(f"-> {result_message['content']}")

            




def generate_content(client, messages):
    response = client.chat.completions.create(
        model = "openrouter/free",
        messages=messages, # type: ignore
        tools = available_functions,
    )
    if not response.usage:
        raise RuntimeError("Failed API request")
    return response


if __name__ == "__main__":
    main()
