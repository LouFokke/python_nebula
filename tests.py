import tkinter as tk
from tkinter import scrolledtext

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Tkinter Example')
        self.geometry('800x600')  # Adjust the window size as needed
        
        # Create the main frame to hold everything
        self.main_frame = tk.Frame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Create a left frame for the large widget
        self.left_frame = tk.Frame(self.main_frame, bg='blue')
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        
        # Create the large widget (use any widget you want here)
        self.large_widget = tk.Label(self.left_frame, text='Large Widget', font=('Helvetica', 20), bg='blue', fg='white')
        self.large_widget.grid(row=0, column=0, sticky="nsew")
        self.left_frame.grid_rowconfigure(0, weight=1)
        self.left_frame.grid_columnconfigure(0, weight=1)
        
        # Create a right frame to hold widgets
        self.right_frame = tk.Frame(self.main_frame)
        self.right_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_columnconfigure(1, weight=1)
        
        # Create the first widget on the right side
        self.widget1 = scrolledtext.ScrolledText(self.right_frame, height=10, width=30)
        self.widget1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.right_frame.grid_rowconfigure(0, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)
        
        # Create the second widget on the right side
        self.widget2 = scrolledtext.ScrolledText(self.right_frame, height=10, width=30)
        self.widget2.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.right_frame.grid_rowconfigure(1, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)
        

if __name__ == "__main__":
    app = App()
    app.mainloop()
