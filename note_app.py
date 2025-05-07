import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

NOTES_FILE = "notes.json"

def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_notes():
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, indent=4)

def add_note():
    title = simpledialog.askstring("New Note", "Enter note title:")
    if title and title not in notes:
        notes[title] = ""
        update_listbox()
        listbox.selection_clear(0, tk.END)
        listbox.selection_set(tk.END)
        load_selected_note()

def delete_note():
    selection = listbox.curselection()
    if selection:
        title = listbox.get(selection)
        if messagebox.askyesno("Delete", f"Delete note '{title}'?"):
            notes.pop(title, None)
            update_listbox()
            text.delete("1.0", tk.END)
            save_notes()

def load_selected_note(event=None):
    selection = listbox.curselection()
    if selection:
        title = listbox.get(selection)
        text.delete("1.0", tk.END)
        text.insert(tk.END, notes.get(title, ""))

def save_current_note():
    selection = listbox.curselection()
    if selection:
        title = listbox.get(selection)
        notes[title] = text.get("1.0", tk.END).strip()
        save_notes()
        messagebox.showinfo("Saved", f"Note '{title}' saved!")

def update_listbox():
    listbox.delete(0, tk.END)
    for title in notes:
        listbox.insert(tk.END, title)

# Load or create notes
notes = load_notes()

# GUI setup
root = tk.Tk()
root.title("Simple Note App")
root.geometry("600x400")

frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

listbox = tk.Listbox(frame, width=30)
listbox.pack(side=tk.LEFT, fill=tk.Y)
listbox.bind("<<ListboxSelect>>", load_selected_note)

text = tk.Text(frame)
text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

tk.Button(btn_frame, text="Add Note", command=add_note).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Delete Note", command=delete_note).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Save", command=save_current_note).pack(side=tk.LEFT, padx=5)

update_listbox()

root.mainloop()
