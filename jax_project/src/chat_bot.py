"""
Terminal based chatbot leveraging Anthropic API.
All configuration logic is loaded via a .env file, allowing for user customization.
"""
import os
import anthropic
from dotenv import load_dotenv


def load_config():
    
    """Load and return configuration values from .env file."""
    
    load_dotenv()
    
    return {
        "model_name": os.getenv("MODEL_NAME"),
        "max_tokens": int(os.getenv("MAX_TOKENS")),
        "system_prompt": os.getenv("SYSTEM"),
    }

def create_client():
    
    """Create and return an authenticated Anthropic client."""
    
    return anthropic.Anthropic()


def get_user_input():
    
    """Prompt for user input. Returns None if user wants to quit/exit."""
    
    user_input = input("You: ").strip()
    if user_input.lower() == "quit" or user_input.lower() == "exit":
        return None
    return user_input or ""


def receive_response(client: anthropic.Anthropic, config: dict, history: list):
    
    """Send conversation history to the API and return the reply text."""
    
    with client.messages.stream(
        model=config["model_name"],
        max_tokens=config["max_tokens"],
        system=config["system_prompt"],
        messages=history,
    ) as stream:
        print("Jax: ", end="", flush=True)
        for text in stream.text_stream:
            print(text, end="", flush=True)
        print("\n")
        return stream.get_final_message().content[0].text


def run_chat_bot():
    
    """Run the interactive terminal chat bot loop."""
    
    config = load_config()
    client = create_client()
    history = []

    print("Chatbot ready. Type 'quit' to exit.\n")

    while True:
        user_input = get_user_input()
        if user_input is None:
            break
        if not user_input:
            continue

        history.append({"role": "user", "content": user_input})
        reply = receive_response(client, config, history)
        history.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    run_chat_bot()
