import sys
import json
import os
from config import MAX_ITERS
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
    for _ in range(20):
        try:
            final_response = generate_content(client, messages, args.verbose)
            if final_response:
                print("Final response: ")
                print(final_response)
                return 
        except Exception as e:
            print(f"Error in generate_content: {e}")

    print(f"Maximum iterations ({MAX_ITERS}) reached")
    sys.exit(1)

            




def generate_content(client, messages, verbose:bool):
    response = client.chat.completions.create(
        model = "openrouter/free",
        messages=messages, # type: ignore
        tools = available_functions,
    )
    if not response.usage:
        raise RuntimeError("Failed API request")
    if verbose:
        print(f"User prompt: {messages[0]['content']}")
        print(f"Prompt tokens:{response.usage.prompt_tokens}") # type: ignore
        print(f"Response tokens: {response.usage.completion_tokens}") # type: ignore
        print("")

    message = response.choices[0].message
    messages.append(message)

    if not message.tool_calls:
        return message.content
    
    
    # print("Response:")
    # print(message.content)
    # print("")

    # print(message.tool_calls) # Example: [ChatCompletionMessageFunctionToolCall(id='call-76eff4e8-cf09-49d3-a697-f68a9584801f', function=Function(arguments='{"file_path":"main.txt","content":"hello"}', name='write_file'), type='function', index=0)]
    # if message.tool_calls:
    for tool_call in message.tool_calls:          
        if tool_call.type != "function":
            continue
        result_message = call_function(tool_call, verbose)
        
        if not result_message['content']:
            raise Exception(f"Empty function response for {tool_call.function.name}")
        if verbose:
            print(f"-> {result_message['content']}")
        messages.append(result_message)

    return None


if __name__ == "__main__":
    main()
