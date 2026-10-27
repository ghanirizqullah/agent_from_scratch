import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse



def main():
    # print("Hello from agent-from-scratch!")
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
            "role": "user",
            "content": args.user_prompt
        }
    ]
    output = generate_content(client, messages)
    if args.verbose:
        print(f"User prompt: {messages[0]['content']}")
        print(f"Prompt tokens:{output.usage.prompt_tokens}")
        print(f"Response tokens: {output.usage.completion_tokens}")
    print("Response:")
    print(output.choices[0].message.content)


def generate_content(client, messages):
    response = client.chat.completions.create(
        model = "openrouter/free",
        messages=messages, # type: ignore
    )
    if not response.usage:
        raise RuntimeError("Failed API request")
    return response


if __name__ == "__main__":
    main()
