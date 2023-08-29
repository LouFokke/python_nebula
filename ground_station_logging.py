

import serial
import time
import tkinter as tk
from PIL import ImageTk, Image
import threading

from tkinter import scrolledtext


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Ground station Nebula')
        self.frame = Window(self)
        self.frame.grid(column=0, row=0, columnspan=2)



class Window(tk.Frame):
    def __init__(self, master):
        super().__init__(master, width=1000, height=500)
        self.master = master

        self.no_connection = ImageTk.PhotoImage(Image.open("sad.gif"))
        self.connection = ImageTk.PhotoImage(Image.open("happy.gif"))

        self.panel = tk.Label(master, image=self.no_connection)
        self.panel.grid(column=0, row=0, columnspan=2)

        self.gps = tk.scrolledtext.ScrolledText(master)
        self.gps.grid(column=0, row=0, padx=150, pady=150, sticky="ew")

        self.altimeter = tk.scrolledtext.ScrolledText(master)
        self.altimeter.grid(column=1, row=0, padx=150, pady=150, sticky="ew")

        self.reception_thread = threading.Thread(target=self.check_reception)
        self.reception_thread.daemon = True  # Daemonize the thread (it will exit when the main program exits)
        self.reception_thread.start()
    
    def check_reception(self):
        serial_port = "COM10"   # Update this to your specific port (e.g., COM1 on Windows)
        baud_rate = 57600       # Set the baud rate to match your device's configuration
        
        # Create a serial object
        ser = serial.Serial(serial_port, baud_rate, timeout=5)
        # Read and print data from the serial port

        while True:
            data = ser.readline().decode().strip()  # Read a line and decode it as a string
            if data == "":
                self.panel.configure(image=self.no_connection)
            else:
                self.panel.configure(image=self.connection)
                self.gps.insert("1.0", f"{data}\n")                

if __name__ == '__main__':
    app = App()
    app.mainloop()

'''

# Define the serial port and baud rate
serial_port = "COM10"  # Update this to your specific port (e.g., COM1 on Windows)
baud_rate = 57600  # Set the baud rate to match your device's configuration

try:
    # Create a serial object
    ser = serial.Serial(serial_port, baud_rate)
    # Read and print data from the serial port
    while True:
        data = ser.readline().decode().strip()  # Read a line and decode it as a string
        print(data)
        
except KeyboardInterrupt:
    print("Keyboard interrupt detected. Closing the serial connection.")
except serial.SerialException as e:
    print(f"An error occurred: {e}")
finally:
    try:
        if ser.is_open:
            ser.close()
    except:
        print('Over')
        pass
'''