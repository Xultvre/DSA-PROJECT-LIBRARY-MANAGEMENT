import json
import os

USER_DB = "data/users.json"

# Initialize User Database
def initialize_users():
    if not os.path.exists(USER_DB):
        with open(USER_DB, "w") as f:
            json.dump({}, f)

# Load Users
def load_users():
    with open(USER_DB, "r") as f:
        return json.load(f)

# Save Users
def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f)

# Signup Function
def signup():
    users = load_users()
    
    role = input("Are you an Admin (yes/no)? ").strip().lower()
    if role == "yes":
        password = input("Enter the authorized password: ").strip()
        if password == "admin123-":
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            users[username] = {"password": password, "role": "admin"}
            save_users(users)
        else:
            print("You are not authorized dear")
            return
        return username, users[username]["role"]

    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    if username in users:
        print(" Username already exists!")
        return None
    users[username] = {"password": password, "role": "user"}
    save_users(users)
    print("Signup successful!")
    return username, users[username]["role"]
    
    
    

# Login Function
def login():
    users = load_users()
    
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    
    if username in users and users[username]["password"] == password:
        print(f"Login successful! Welcome, {username}.")
        return username, users[username]["role"]
    
    print("Invalid username or password.")
    return None

def remove_user(target_username, current_admin):
    users = load_users()
    if target_username not in users:
        print(" User does not exist.")
        return
    if target_username == current_admin:
        print(" You cannot remove your own account.")
        return
    if users[target_username]["role"] == "admin":
        print(" You cannot remove another admin.")
        return
    del users[target_username]
    save_users(users)
    print(f"User '{target_username}' has been removed.")
