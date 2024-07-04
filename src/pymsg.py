import requests
import json
import tkinter as tk
from tkinter import scrolledtext, messagebox

TUNNEL_URL = 'INSERT_TUNNEL_URL_HERE'
username = None
password = None

def login(username, password):
    url = f'{TUNNEL_URL}/login'
    payload = {'username': username, 'password': password}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        print("Error decoding JSON. Response content:")
        print(response.text)
        return {'status': 'Error'}

def send_message(username, message):
    url = f'{TUNNEL_URL}/send'
    payload = {'username': username, 'message': message}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        print("Error decoding JSON. Response content:")
        print(response.text)
        return {'status': 'Error'}

def receive_messages():
    url = f'{TUNNEL_URL}/receive'
    response = requests.get(url)
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        print("Error decoding JSON. Response content:")
        print(response.text)
        return []

def login_gui():
    global username, password
    username = entry_username.get()
    password = entry_password.get()
    response = login(username, password)
    if response.get('status') == f'Logged in as {username}':
        messagebox.showinfo("Success", f"Successfully logged in as {username}")
        root.deiconify()
        login_window.destroy()
    else:
        messagebox.showerror("Error", f"Error: {response.get('status')}")
        username = None
        password = None

def send_message_gui():
    message = entry_message.get()
    response = send_message(username, message)
    if response.get('status') == 'Message received':
        entry_message.delete(0, tk.END)
        refresh_messages()
    else:
        messagebox.showerror("Error", f"Error: {response.get('status')}")

def refresh_messages():
    messages = receive_messages()
    text_messages.config(state=tk.NORMAL)
    text_messages.delete(1.0, tk.END)
    for msg in messages:
        text_messages.insert(tk.END, f"{msg['username']}: {msg['message']}\n")
    text_messages.config(state=tk.DISABLED)
    root.after(2000, refresh_messages)  # Refresh every 2 seconds

# Login window
login_window = tk.Tk()
login_window.title("Login to PyMsg")

tk.Label(login_window, text="Username:").pack(padx=10, pady=5)
entry_username = tk.Entry(login_window)
entry_username.pack(padx=10, pady=5)

tk.Label(login_window, text="Password:").pack(padx=10, pady=5)
entry_password = tk.Entry(login_window, show='*')
entry_password.pack(padx=10, pady=5)

tk.Button(login_window, text="Login", command=login_gui).pack(padx=10, pady=10)

# Main window
root = tk.Tk()
root.title("PyMsg")
root.geometry("400x400")

text_messages = scrolledtext.ScrolledText(root, state=tk.DISABLED)
text_messages.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

frame_message = tk.Frame(root)
frame_message.pack(padx=10, pady=5, fill=tk.X)

entry_message = tk.Entry(frame_message)
entry_message.pack(side=tk.LEFT, fill=tk.X, expand=True)
tk.Button(frame_message, text="Send", command=send_message_gui).pack(side=tk.LEFT, padx=5)

tk.Button(root, text="Refresh", command=refresh_messages).pack(padx=10, pady=10)

root.withdraw()  # Hide the main window initially
root.after(2000, refresh_messages)  # Refresh messages every 2 seconds

login_window.mainloop()
