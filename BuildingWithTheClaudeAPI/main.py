import json

from dotenv import load_dotenv
from anthropic import Anthropic


def add_user_message(messages, text):
    user_message = {"role":"user", "content": text}
    messages.append(user_message)

def add_assistant_message(messages, text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)

def chat(messages, system=None, temperature=None, stop_sequences=None):

    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
        "temperature": temperature,
        "stop_sequences": stop_sequences,
    }

    if system:
        params["system"] = system

    message = client.messages.create(**params)
    return message.content[0].text

def generate_dataset():
    prompt = ""
    temperature = 0.0
    print(">> Provide a prompt for generating the dataset or press Enter for default prompt.")
    prompt = input("> ")

    if prompt == "":
        prompt="""
    Generate an evaluation dataset for prompt evaluation. the dataset will be used to evaluate a prompt that generate Python,
    JSON, or Regex specifically for AWS-related tasks. Generate an array of JSON each representing a task that requires Python, 
    JSON, or Regex to complete.
    
    Example output:
    ```json
    [
        {
            "task" : "Desscription of task",
        },
        ...additional
    ]
    ```
    
    * Focus on tasks that can be solved by writing a single Python function, a single JSON object, of a single Regex.
    * Focus on tasks that do not require writing much code.
    
    Please generate 3 objects.
        """

    add_user_message(messages, prompt)
    add_assistant_message(messages, "```json")
    text = chat(messages, stop_sequences=["```"], temperature=temperature)
    return json.loads(text)

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
    temperature = 0.0
    messages = []

    dataset = generate_dataset()
    print(dataset)





