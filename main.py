from customtkinter import *
import json
import os

class App:
  def __init__(self, master):
    self.master = master
    self.master.title("Todo App")
    self.master.geometry("400x500")
    set_appearance_mode("dark")
    set_default_color_theme("blue")

    self.data_file = "data.json"
    self.todos = self.load_todos()
    self.todos_label = []
    self.status = []
    self.create_ui()
    self.refresh_scrollframe()
    self.message_var = StringVar(value="")
    self.message_label = CTkLabel(self.master, textvariable=self.message_var, text_color="white", font=("Arial", 14))
    self.message_label.pack(pady=(0, 5))

  def load_todos(self):
    if os.path.exists(self.data_file):
        with open(self.data_file, "r") as f:
            try:
                return json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                return []
    return []

  def save_data(self):
    with open(self.data_file, "w") as f:
        json.dump(self.todos, f, indent=4)

  def create_ui(self):
    self.label = CTkLabel(self.master, text="This app is under development", font=("Arial", 20, 'bold'), fg_color="transparent", text_color="red")
    self.label.pack(padx=5, pady=10)
    
    self.todoentry = CTkEntry(self.master, width=300)
    self.todoentry.configure(font=("Arial", 15))
    self.todoentry.pack(padx=5, pady=10)

    self.addbtn = CTkButton(self.master, text="+ Add", command=self.add)
    self.addbtn.configure(font=("Arial", 15))
    self.addbtn.pack(padx=5, pady=10)

    self.removebtn = CTkButton(self.master, text="- Remove", command=self.remove)
    self.removebtn.configure(font=("Arial", 15))
    self.removebtn.pack(padx=5, pady=10)

    self.scroll_frame = CTkScrollableFrame(self.master)
    self.scroll_frame.pack(fill=BOTH, expand=True)

  def show_message(self, text, color="white"):
    self.message_var.set(text)
    self.message_label.configure(text_color=color)
    self.master.after(3000, lambda: self.message_var.set(""))

  def add(self):
    todo_name = self.todoentry.get().title().strip()
    if not todo_name:
      self.show_message("Please enter a todo name.", "orange")
      return
    if any(todo["name"] == todo_name for todo in self.todos):
      self.show_message(f"{todo_name} already exists.", "red")
      return
    self.todos.append({"name": todo_name, "done": False})
    self.save_data()
    self.todoentry.delete(0, END)
    self.refresh_scrollframe()
    self.show_message(f"{todo_name} added successfully!", "green")

  def remove(self):
    todo_name = self.todoentry.get().title().strip()
    if not todo_name:
      self.show_message("Please enter a todo name.", "orange")
      return
    if todo_name not in self.todos:
      self.show_message("No todo with this name.", "orange")
    self.todos.remove({"name": todo_name, "done": False})
    self.save_data()
    self.todoentry.delete(0, END)
    self.refresh_scrollframe()
    self.show_message(f"{todo_name} removed successfully!", "green")

  def refresh_scrollframe(self):
    for widget in self.todos_label:
      widget.destroy()
    self.todos_label.clear()

    for todo in self.todos:
      checkbox = CTkCheckBox(self.scroll_frame, text=todo["name"], font=("Arial", 14), onvalue=True, offvalue=False)
      checkbox.pack(fill="x", padx=10, pady=5)
      self.todos_label.append(checkbox)
      checkbox.select() if todo["done"] else checkbox.deselect()


if __name__ == "__main__":
  root = CTk()
  app = App(root)
  root.mainloop()