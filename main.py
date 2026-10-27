import os
from dotenv import load_dotenv
from openai import OpenAI



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

    prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

    response = client.chat.completions.create(
        model = "openrouter/free",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    if not response.usage:
        raise RuntimeError("Failed API request")
    print(f"User prompt: {prompt}")
    print(f"Prompt tokens:{response.usage.prompt_tokens}")
    print(f"Response tokens: {response.usage.completion_tokens}")
    print("Response:")
    print(response.choices[0].message.content)
if __name__ == "__main__":
    main()
