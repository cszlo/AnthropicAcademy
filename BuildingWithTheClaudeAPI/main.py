from dotenv import load_dotenv
from anthropic import Anthropic


def add_user_message(messages, text):
    user_message = {"role":"user", "content": text}
    messages.append(user_message)

def add_assistant_message(messages, text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)

def chat(messages, system=None, temperature=None, stream=True):

    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
        "temperature": temperature,
        "stream": stream
    }

    if system:
        params["system"] = system

    stream = client.messages.create(**params)
    # Print response
    for event in stream:
        if event.delta.text:
            print(event.delta.text)


# When working with the Anthropic API and Claude, there's a crucial concept
# you need to understand: Claude doesn't store any of your conversation history.
# Each request you make is completely independent, with no memory of previous
# exchanges. This means if you want to have a multi-turn conversation where Claude
# remembers context from earlier messages, you need to handle the conversation
# state yourself.
if __name__ == '__main__':
    load_dotenv()
    client = Anthropic()
    model = "claude-sonnet-4-0"
    temperature = 1.0
    messages = []

    print(">> Provide a system prompt (or not). Example: 'You are a patient math tutor. Do not directly answer a student's questions. Guide them to a solution step by step.'")
    system = input("> ")

    print("Preparing Chat bot...")
    print("Send 'exit' to quit session.")

    while True:
        print()
        user_input = input("> ")
        if user_input.lower() == 'exit':
            print(">> Goodbye!")
            break

        # Prepare, send and capture a request to Anthropic API.
        add_user_message(messages, user_input)

        with client.messages.stream(
                model=model,
                max_tokens=1000,
                messages=messages,
        ) as stream:
            for text in stream.text_stream:
                print(text, end="")
                pass

        # stream.get_final_message())

        # Add assistant response to conversation history.
        # add_assistant_message(messages, stream.get_final_message())








