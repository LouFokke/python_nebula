import serial
import time
import tkinter as tk
from PIL import ImageTk, Image
import threading
import numpy as np

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
        self.current_log_name = f'{datetime.now().strftime("%Y-%m-%d %Hh%Mm%Ss")}.txt'

        master.grid_rowconfigure(0, weight=1)
        master.grid_rowconfigure(1, weight=0)
        master.grid_rowconfigure(2, weight=1)
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)
        master.grid_columnconfigure(2, weight=1)
        master.grid_columnconfigure(3, weight=1)

        self.no_connection = ImageTk.PhotoImage(Image.open("images/no.gif").resize((master.width, master.height)))
        self.connection = ImageTk.PhotoImage(Image.open("images/yes.gif").resize((master.width, master.height)))

        self.panel = tk.Label(master, image=self.no_connection)
        self.panel.grid(column=0, row=0, columnspan=5, rowspan=3, sticky='nsew')

        self.gps = tk.scrolledtext.ScrolledText(master, height=25, width=50, state=tk.DISABLED)
        self.gps.grid(column=0, row=0, columnspan=2, rowspan=2, padx=(100, 50), pady=(75, 5), sticky="nsew")

        self.altimeter = tk.scrolledtext.ScrolledText(master, height=25, width=50, state=tk.DISABLED)
        self.altimeter.grid(column=2, row=0, columnspan=2, padx=(50, 5), pady=(75, 25), sticky="nsew")
        self.altitudes = []             # Altitudes are stored in feet

        self.flight_altitude = tk.scrolledtext.ScrolledText(master, height=25, width=20, state=tk.DISABLED, fg='green')
        self.flight_altitude.grid(column=4, row=0, padx=(5, 100), pady=(75, 25), sticky='nsew')
        self.start_altitude = None

        instantaneous_label = tk.Label(master, height=2, width=25, text='Instantaneous speed (m/s)', font=('menlo', 15))
        instantaneous_label.grid(column=2, row=1, padx=(50, 5), pady=(5, 5), sticky='nsew')

        average_label = tk.Label(master, height=2, width=25, text='Average speed (m/s)', font=('menlo', 15))
        average_label.grid(column=3, row=1, columnspan=2, padx=(5, 100), pady=(5, 5), sticky='nsew')
        
        self.instant_speed = tk.Label(master, height=5, width=25, text='', font=('menlo', 15))
        self.instant_speed.grid(column=2, row=2, padx=(50, 5), pady=(5, 75), sticky='nsew')

        self.average_speed = tk.Label(master, height=5, width=25, text='', font=('menlo', 15))
        self.average_speed.grid(column=3, row=2, columnspan=2, padx=(5, 100), pady=(5, 75), sticky='nsew')

        start_frame = tk.Frame(master, height=12, width=250)
        start_frame.pack_propagate(0)
        start_frame.grid(column=1, row=2, padx=(5, 50), pady=(5, 75), sticky='nsew')

        start_button = tk.Button(start_frame, text='LAUNCH', font=('menlo', 35), bg='red',
                     command=self.launch)
        start_button.pack(fill="both", expand=True)
        self.start = False
        
        tplus_frame = tk.Frame(master, height=12, width=400)
        tplus_frame.pack_propagate(0)
        tplus_frame.grid(column=0, row=2, padx=(100, 5), pady=(5, 75), sticky='nsew')

        self.tplus = tk.Label(tplus_frame, text='STANDBY', fg='green', font=('menlo', 50))
        self.tplus.pack(fill='both', expand=True)

        self.reception_thread = threading.Thread(target=self.check_reception)
        self.reception_thread.daemon = True
        self.reception_thread.start()

    def check_reception(self):
        '''
        Check constantly if data is being received.
        '''
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
                self.manage_received_data(data)

    def manage_received_data(self, data: str):
        '''
        Store the received data in the logs.txt file and if the data is valid, display on the scrolledtext widgets.
        '''
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-5]
        stripped_data = data.split(' ')
        # if int(stripped_data[1]) % 2 == 0:      # Remove half the data
        if self.data_is_valid(stripped_data):
            self.update_scrolledtext_with_serial_data(stripped_data, date)
            self.altitudes.append([datetime.now(), float(stripped_data[10])])
            self.update_speeds()
            
        save_file = open(self.current_log_name, 'a')
        save_file.write(f'{date} -- {data}\n')
        save_file.close()
    
    def data_is_valid(self, stripped_data: list):
        '''
        Check if the data received by serial is valid.
        '''
        right_len = len(stripped_data) == 12
        right_elements = (stripped_data[0] == '&' and stripped_data[2] == '&' and stripped_data[5] == '&' 
                          and stripped_data[8] == '&' and stripped_data[11] == '&')
        return right_len and right_elements
    
    def update_scrolledtext_with_serial_data(self, stripped_data: list, date):
        '''
        Update the scrolledtext widgets by making use of the serial data.
        '''
        self.gps.config(state=tk.NORMAL)
        self.gps.insert("1.0", f'{date} -- Latitude: {stripped_data[4]}, Longitude {stripped_data[7]}\n')
        self.gps.config(state=tk.DISABLED)

        self.altimeter.config(state=tk.NORMAL)
        self.altimeter.insert("1.0", f"{date} -- Altitude: {stripped_data[10]} ft\n")
        self.altimeter.config(state=tk.DISABLED)

        if self.start_altitude is not None:
            if self.altitudes[-1][1] - self.altitudes[-2][1] >= 0:
                color = "green" 
            else:
                color = "red"

            self.flight_altitude.config(state=tk.NORMAL)
            self.flight_altitude.tag_configure(color, foreground=color)
            self.flight_altitude.insert("1.0", f"{float(stripped_data[10]) - self.start_altitude} ft\n", (color,))
            self.flight_altitude.config(state=tk.DISABLED)
    
    def update_speeds(self):
        '''
        Update the two speed values.
        '''
        raw_altitudes = np.array(self.altitudes)
        altitudes = np.stack((raw_altitudes[:,0], raw_altitudes[:,1]*0.3048), axis=1)
            
        # Update the instant speed label first
        if altitudes.shape[0] >= 2:
            time_delta = (altitudes[-1,0] - altitudes[-2,0]).total_seconds()
            altitude_delta = altitudes[-1,1] - altitudes[-2,1]
            self.instant_speed.config(text=round(altitude_delta / time_delta, 2))
        
        # Update the average speed label second
        if altitudes.shape[0] >= 11:
            deltas = altitudes[-10:,:] - altitudes[-11:-1,:]
            average_speed = deltas[:,1] / np.vectorize(lambda dt: dt.total_seconds())(deltas[:,0])  
            self.average_speed.config(text=round(np.mean(average_speed), 2))

    def launch(self):
        '''
        Initialize the time counter and set the start altitude.
        '''
        if not self.start:
            self.start = True
            self.start_altitude = self.altitudes[-1][1]
            save_file = open(self.current_log_name, 'a')
            writing_str = '-'*50 + f'\nLaunch at {datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-5]}\n' \
                            + '-'*50 + '\n'
            save_file.write(writing_str)
            save_file.close()

            self.reception_thread = threading.Thread(target=self.count)
            self.reception_thread.daemon = True
            self.reception_thread.start()

    def count(self):
        '''
        Count the seconds since count initialization.
        '''
        seconds = 0
        while True:
            self.tplus.config(text=self.format_time(seconds))
            time.sleep(1)
            seconds += 1

    def format_time(self, seconds):
        '''
        Format the number of seconds into hh:mm:ss format.
        '''
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f'T+{hours:02d}:{minutes:02d}:{seconds:02d}'



if __name__ == '__main__':
    app = App()
    app.mainloop()



'''
self.manage_received_data('& 502 & Lat: 48.476062 & Long: -81.336410 & alt: 1157.8 &')
time.sleep(0.1)
self.manage_received_data('& 503 & Lat: 49.476062 & Long: -82.336410 & alt: 1158.8 &')
time.sleep(0.1)
self.manage_received_data('& 504 & Lat: 49.476062 & Long: -82.336410 & alt: 1159.8 &')
time.sleep(0.1)
self.manage_received_data('& 505 & Lat: 49.476062 & Long: -82.336410 & alt: 1160.8 &')
time.sleep(0.1)
self.manage_received_data('& 506 & Lat: 49.476062 & Long: -82.336410 & alt: 1161.8 &')
time.sleep(0.1)
self.manage_received_data('& 507 & Lat: 49.476062 & Long: -82.336410 & alt: 1162.8 &')
time.sleep(0.1)
self.manage_received_data('& 508 & Lat: 49.476062 & Long: -82.336410 & alt: 1163.8 &')
time.sleep(0.1)
self.manage_received_data('& 509 & Lat: 49.476062 & Long: -82.336410 & alt: 1164.8 &')
time.sleep(0.1)
self.manage_received_data('& 510 & Lat: 49.476062 & Long: -82.336410 & alt: 1165.8 &')
time.sleep(0.1)
self.manage_received_data('& 511 & Lat: 49.476062 & Long: -82.336410 & alt: 1166.8 &')
time.sleep(0.1)
self.manage_received_data('& 512 & Lat: 49.476062 & Long: -82.336410 & alt: 1167.8 &')
self.update_speeds()
'''