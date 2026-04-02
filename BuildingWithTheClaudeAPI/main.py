from dotenv import load_dotenv
from anthropic import Anthropic


def add_user_message(messages, text):
    user_message = {"role":"user", "content": text}
    messages.append(user_message)

def add_assistant_message(messages, text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)

def chat(messages):
    message = client.messages.create(
        model=model,
        max_tokens=1000,
        messages=messages
    )
    return message.content[0].text


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
    messages = []

    # Prepare, send and capture a request to Anthropic API.
    add_user_message(messages, "Tell me about agentic AI in 2-3 sentences.")
    answer = chat(messages)

    # Print response
    print(answer)

    # Prepare, send and capture a follow-up request to Anthropic API.
    add_assistant_message(messages, answer)
    add_user_message(messages, "How long has it been around?")
    answer = chat(messages)

    # Print response
    print(answer)



