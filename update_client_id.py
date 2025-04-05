import tkinter as tk
from tkinter import ttk, messagebox
import json

CONFIG_FILE = 'config.json'

def load_config():
    try:
        with open(CONFIG_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"client_id": "1314279361582596146"}

def save_config(config):
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config, file, indent=4)

class ClientIDUpdaterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Update Discord Client ID")
        self.geometry("300x150")

        self.client_id_label = tk.Label(self, text="Discord Client ID:")
        self.client_id_label.pack(pady=5)
        self.client_id_entry = tk.Entry(self)
        self.client_id_entry.pack(pady=5)

        config = load_config()
        self.client_id_entry.insert(0, config['client_id'])

        self.update_button = ttk.Button(self, text="Update Client ID", command=self.update_client_id)
        self.update_button.pack(pady=10)

    def update_client_id(self):
        new_client_id = self.client_id_entry.get().strip()
        if new_client_id:
            config = {"client_id": new_client_id}
            save_config(config)
            messagebox.showinfo("Success", "Client ID updated successfully!")
        else:
            messagebox.showerror("Error", "Client ID cannot be empty.")

if __name__ == "__main__":
    app = ClientIDUpdaterApp()
    app.mainloop()
