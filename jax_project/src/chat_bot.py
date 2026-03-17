"""
Terminal based chatbot leveraging Anthropic API.
All configuration logic is loaded via a .env file, allowing for user customization.
"""
import os
import anthropic
from dotenv import load_dotenv
from src import database
import time

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

def get_user_name():
    
    """Captures user first and last name for DB storage."""
    
    print("Hello! Please enter First and Last Name to begin session.\n")
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    return first_name, last_name

def get_user_input():
    
    """Prompt for user input. Returns None if user wants to quit/exit."""
    
    user_input = input("You: ").strip()
    if user_input.lower() == "quit" or user_input.lower() == "exit":
        return None
    return user_input or ""


def receive_response(client: anthropic.Anthropic, config: dict, history: list):
    
    """Stream a response from the Anthropic API."""
    #Capture start of message
    start_time = time.perf_counter()
    
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
        final_message = stream.get_final_message()
        
        #Capture time of message stream
        end_time = time.perf_counter()
        
        #Capture tokens and reply assign to variables
        reply = final_message.content[0].text
        input_tokens = final_message.usage.input_tokens
        output_tokens = final_message.usage.output_tokens
        
        #latency calculation
        latency_ms = (end_time - start_time) * 1000
        
        #Return reply response from LLM, input tokens, output tokens, and latency of transaction
        return (reply, input_tokens, output_tokens, latency_ms)
    
def run_chat_bot():
    
    """Run the interactive terminal chat bot loop."""
    
    config = load_config()
    client = create_client()
    history = []
    
    #Database integration calls
    database.init_db()
    first_name, last_name = get_user_name()
    user_id = database.insert_users(first_name, last_name)
    session_id = database.insert_sessions(user_id, config["model_name"])
    
    print("\nChatbot ready. Type 'quit' or 'exit' to end session.\n")

    while True:
        user_input = get_user_input()
        if user_input is None:
            break
        if not user_input:
            continue
        
        history.append({"role": "user", "content": user_input})
        reply, input_tokens, output_tokens, latency_ms = receive_response(client, config, history)
        
        #Store into databases
        message_id = database.insert_messages(session_id, user_input, input_tokens)
        database.insert_responses(message_id, reply, output_tokens, latency_ms)
        
        history.append({"role": "assistant", "content": reply})

if __name__ == "__main__":
    run_chat_bot()
