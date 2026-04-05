"""
Terminal based chatbot leveraging Anthropic API.
All configuration logic is loaded via a .env file, allowing for user customization.
"""
import os
import anthropic
from dotenv import load_dotenv
<<<<<<< HEAD
import database
import time
=======

>>>>>>> 8cad3eb8fbcaa97f85d6630fb41f9f6dc7dd1be3

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
<<<<<<< HEAD
    
    #Database integration calls
    database.init_db()
    first_name, last_name = get_user_name()
    
    user_id = database.find_users(first_name, last_name)                            
    if user_id is None:                                                             
        user_id = database.insert_users(first_name, last_name) 
    
    session_id = database.insert_sessions(user_id, config["model_name"])
    
    history = database.get_prior_history(user_id)
    
    print("\nChatbot ready. Type 'quit' or 'exit' to end session.\n")
=======
    history = []

    print("Chatbot ready. Type 'quit' to exit.\n")
>>>>>>> 8cad3eb8fbcaa97f85d6630fb41f9f6dc7dd1be3

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
