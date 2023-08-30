import tkinter as tk
from tkinter import scrolledtext

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Colored Text Example")

        self.text = scrolledtext.ScrolledText(self, wrap=tk.WORD)
        self.text.pack()

        # Insert colored text
        self.insert_colored_text("Hello, ", "blue")
        self.insert_colored_text("world!", "red")

    def insert_colored_text(self, text, color):
        # Configure a tag with the specified color
        self.text.tag_configure(color, foreground=color)

        # Insert text with the configured tag
        self.text.insert(tk.END, text, (color,))

if __name__ == '__main__':
    app = App()
    app.mainloop()
