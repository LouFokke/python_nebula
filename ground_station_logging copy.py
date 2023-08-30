

import serial
import time
import tkinter as tk
from PIL import ImageTk, Image
import threading

from tkinter import scrolledtext
from datetime import datetime


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.width = 1500
        self.height = 750
        self.title('Ground station Nebula')
        self.frame = Window(self)
        self.frame.grid(column=0, row=0)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)



class Window(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.no_connection = ImageTk.PhotoImage(Image.open("images/no.gif").resize((master.width, master.height)))
        self.connection = ImageTk.PhotoImage(Image.open("images/yes.gif").resize((master.width, master.height)))

        self.panel = tk.Label(master, image=self.no_connection)
        self.panel.grid(column=0, row=0, columnspan=2, sticky='nsew')

        self.gps = tk.scrolledtext.ScrolledText(master, height=25, width=50)
        self.gps.grid(column=0, row=0, padx=(150,75), pady=150, sticky="nsew")

        self.right_frame = tk.Frame(master, height=25, width=500)
        self.right_frame.grid(column=1, row=0, padx=(75,150), pady=150, sticky="nsew")

        self.right_frame.altimeter = tk.scrolledtext.ScrolledText(self.right_frame, height=25, width=50)
        self.right_frame.altimeter.grid(column=0, row=0, columnspan=2, pady=(0,10), sticky="nsew")

        tk.Label(self.right_frame, height=25, width=25, text='1').grid(column=0, row=1, sticky='nsew')

       # self.right_frame.

        '''

        self.manage_data('& 502 & Lat: 48.476062 & Long: -81.336410 & alt: 1157.8 &')
        self.manage_data('& 503 & Lat: 49.476062 & Long: -82.336410 & alt: 1158.8 &')
       # raise


        self.reception_thread = threading.Thread(target=self.check_reception)
        self.reception_thread.daemon = True  # Daemonize the thread (it will exit when the main program exits)
        self.reception_thread.start()'''
    
    def check_reception(self):
        serial_port = "COM10"   # Update this to your specific port (e.g., COM1 on Windows)
        baud_rate = 57600       # Set the baud rate to match your device's configuration
        
        # Create a serial object
        ser = serial.Serial(serial_port, baud_rate, timeout=5)
        # Read and print data from the serial port

        while True:
            data = ser.readline().decode().strip()  # Read a line and decode it as a string
            if data == "":      # Timeout
                self.panel.configure(image=self.no_connection)
            else:
                self.panel.configure(image=self.connection)
                self.manage_data(data) 

    def manage_data(self, data: str):
        stripped_data = data.split(' ')
        if self.data_is_valid(stripped_data):
            self.format_data(stripped_data)
        
        save_file = open('logs.txt', 'a')
        save_file.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-5]} -- {data}\n')
    
    def data_is_valid(self, stripped_data: list):
        right_len = len(stripped_data) == 12
        right_elements = (stripped_data[0] == '&' and stripped_data[2] == '&' and stripped_data[5] == '&' 
                          and stripped_data[8] == '&' and stripped_data[11] == '&')
        return right_len and right_elements
    
    def format_data(self, stripped_data: list):
        self.gps.insert("1.0", f"Latitude: {stripped_data[4]}, Longitude {stripped_data[7]}\n")
        self.altimeter.insert("1.0", f"Altitude: {stripped_data[10]} ft\n")

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