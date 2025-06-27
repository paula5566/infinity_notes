import tkinter as tk
from tkinter import ttk, filedialog, font, messagebox

class InfinityNotesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Infinity Notes")
        self.root.geometry("800x600")
        self.dark_mode = False

        self.default_font = font.Font(family="Arial", size=12)
        self.header_font = font.Font(family="Arial", size=16, weight="bold")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)

        file_menu = tk.Menu(self.menu_bar, tearoff=False)
        file_menu.add_command(label="New Tab", command=self.new_tab)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Close Tab", command=self.close_tab)  # Added here
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        self.theme_button = tk.Button(root, text="🌙 Dark Mode", command=self.toggle_theme)
        self.theme_button.pack(side="bottom", fill="x")

        self.close_button = tk.Button(root, text="❌ Close Tab", command=self.close_tab)
        self.close_button.pack(side="bottom", fill="x")  # Optional button

        self.new_tab()

    def new_tab(self):
        frame = ttk.Frame(self.notebook)
        text = tk.Text(frame, font=self.default_font, wrap="word")
        text.pack(fill="both", expand=True)

        text.bind("<Shift-Return>", self.check_for_header)

        self.notebook.add(frame, text=f"Tab {len(self.notebook.tabs()) + 1}")
        self.notebook.select(len(self.notebook.tabs()) - 1)
        self.apply_theme(text)

    def get_current_text_widget(self):
        current_tab = self.notebook.select()
        return self.notebook.nametowidget(current_tab).winfo_children()[0]

    def check_for_header(self, event=None):
        widget = self.get_current_text_widget()
        index = widget.index("insert linestart")
        line_text = widget.get(index, f"{index} lineend")

        if line_text.strip().startswith("#"):
            header_text = line_text.lstrip("#").lstrip()
            widget.delete(index, f"{index} lineend")
            widget.insert(index, header_text)
            widget.tag_add("header", index, f"{index} + {len(header_text)}c")
            widget.tag_config("header", font=self.header_font)
            return "break"
        else:
            return None

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        for tab_id in self.notebook.tabs():
            text = self.notebook.nametowidget(tab_id).winfo_children()[0]
            self.apply_theme(text)

        if self.dark_mode:
            self.theme_button.config(text="☀️ Light Mode")
        else:
            self.theme_button.config(text="🌙 Dark Mode")

    def apply_theme(self, text_widget):
        if self.dark_mode:
            text_widget.config(bg="#1e1e1e", fg="#d4d4d4", insertbackground="white")
        else:
            text_widget.config(bg="white", fg="black", insertbackground="black")

    def open_file(self):
        file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file:
            with open(file, "r") as f:
                self.new_tab()
                text = self.get_current_text_widget()
                text.insert(tk.END, f.read())

    def save_file(self):
        file = filedialog.asksaveasfilename(defaultextension=".txt")
        if file:
            text = self.get_current_text_widget()
            with open(file, "w") as f:
                f.write(text.get(1.0, tk.END))

    def close_tab(self):
        if self.notebook.index("end") > 1:
            current = self.notebook.select()
            self.notebook.forget(current)
        else:
            messagebox.showinfo("Info", "Can't close the last tab.")

# Run it
root = tk.Tk()
app = InfinityNotesApp(root)
root.mainloop()
