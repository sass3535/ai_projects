"""
    Databse instance created for historical context persistance
    for chatbot
"""
import sqlite3
import os

#Definitions for tables and database name
db = "jax_history.db"

#Table and schema creation variables
users_create = "CREATE TABLE IF NOT EXISTS Users(id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT, last_name TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP)"
sessions_create = "CREATE TABLE IF NOT EXISTS Sessions(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER REFERENCES Users(id), created_at TEXT DEFAULT CURRENT_TIMESTAMP, model_name TEXT)"
messages_create = "CREATE TABLE IF NOT EXISTS Messages(id INTEGER PRIMARY KEY AUTOINCREMENT, session_id INTEGER REFERENCES Sessions(id), content TEXT, timestamp TEXT DEFAULT CURRENT_TIMESTAMP, token_count INTEGER)"
responses_create = "CREATE TABLE IF NOT EXISTS Responses(id INTEGER PRIMARY KEY AUTOINCREMENT, message_id INTEGER REFERENCES Messages(id), content TEXT, timestamp TEXT DEFAULT CURRENT_TIMESTAMP, token_count INTEGER, latency_ms REAL)"

#Insert variables using ? parameter placeholder for values
users_insert = "INSERT INTO Users(first_name, last_name) VALUES (?,?)"
sessions_insert = "INSERT INTO Sessions(user_id, model_name) VALUES (?,?)"
messages_insert = "INSERT INTO Messages(session_id, content, token_count) VALUES (?,?,?)"
responses_insert = "INSERT INTO Responses(message_id, content, token_count, latency_ms) VALUES (?,?,?,?)"

#Constant for DB path placement, consistently place DB in jax_project sub directory
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), db)

#Connect to database instance if no db exists, connect to it, ensure foreign keys are activated
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

#Create tables inside db and setup db schema, permanently save any changes made to DB during current transaction
def init_db():
    with get_connection() as connection:
        cursor = connection.cursor()
        
        cursor.execute(users_create)
        cursor.execute(sessions_create)
        cursor.execute(messages_create)
        cursor.execute(responses_create)

        connection.commit()

#Insert values into users table
def insert_users(first_name, last_name):
    with get_connection() as connection:
        cursor = connection.cursor()
        
        cursor.execute(users_insert, (first_name, last_name))
        connection.commit()
        
        return cursor.lastrowid

#Insert values into sessions table
def insert_sessions(user_id, model_name):
    with get_connection() as connection:
        cursor = connection.cursor()
        
        cursor.execute(sessions_insert, (user_id, model_name))
        connection.commit()
        
        return cursor.lastrowid
    
#Insert values into messages table
def insert_messages(session_id, content, token_count):
    with get_connection() as connection:
        cursor = connection.cursor()
        
        cursor.execute(messages_insert, (session_id, content, token_count))
        connection.commit()
        
        return cursor.lastrowid

#Insert values into responses table
def insert_responses(message_id, content, token_count, latency_ms):
    with get_connection() as connection:
        cursor = connection.cursor()
        
        cursor.execute(responses_insert, (message_id, content, token_count, latency_ms))
        connection.commit()
        
        return cursor.lastrowid

#Test block for functions above
# if __name__ == "__main__":
#     init_db()                                
#     user_id = insert_users("Matt", "Sassoon")
#     session_id = insert_sessions(user_id,"claude-opus-4-6")
#     message_id = insert_messages(session_id, "Hello", 6)
#     insert_responses(message_id, "Hello back", 6, 3.74)