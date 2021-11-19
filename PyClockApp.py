##############===----Time Clock App Overview----===###################
#   aNIYAH FLIGHT CONFIRMATION GYGBRH  PIN 0908  
# cHANGE UNACCOMPANIED NUMBER 8003258847  
'''
    References 
    https://tkdocs.com/tutorial/index.html
    https://pyvisa.readthedocs.io/en/latest/introduction/index.html
    https://www.codegrepper.com/code-examples/python/how+to+append+a+list+to+a+text+file+in+python
    DO NEED TO CREATE EXTERNAL DOCUMENTAION FOR THE ENTIRE APP
'''
import os
import datetime as dt
import time 
import pyvisa
import math as math
from tkinter import *
import tkinter as tk
from tkinter import ttk, filedialog, Text, messagebox

rm = pyvisa.ResourceManager()
rm.list_resources()

def convertTuple(usb):
    ''' Converts 53230A USB Address tuple into string'''
    str = ''
    for item in usb:
        str = str + item
    return str
freq_counter_usb = convertTuple(rm.list_resources()[0])

try:
    freq_counter = rm.open_resource(freq_counter_usb)
except pyvisa.errors.VisaIOError:
    print("The 53230A Frequency Counter is not found!\nPlease check for connection.")
    messagebox.showinfo("Fail!",message="USB Address was incorrect, please check the connection!")

root = Tk()
root.title("Clock Trip Calibration")
photo = PhotoImage(file = "C:/Users/KaiHall/PyApp/PyClockApp/clock.png")
root.iconphoto(False, photo)
mainframe = ttk.Frame(root, padding="10 4 4 4")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

class FC:

    '''Keysight 53230A Universal Frequency Counter/Timer Gui Time Interval measurment '''

    output_fileloc = StringVar() 
    ch_signal = IntVar()
    measurement_mode = IntVar()
    measure_mode = IntVar()
    user_fileloc = StringVar()
    seconds_spin = IntVar()
    samples_spin = IntVar()
    avg_spin = IntVar()
    sample_output = StringVar()
    output_fileloc = StringVar()
    ch1_signal = IntVar()
    ch2_signal = IntVar()
    progress_bar = IntVar()
    user_input_mintues = IntVar()
    user_input_hours = IntVar()
    average_sample = IntVar()
    mjd = float()
    current_date = 0
    samples_run = IntVar()
    measurement_start_time = IntVar()
    timeout_min = IntVar()
    timeout_hrs = float()
    timeout_start = float()
    file_string = StringVar()
    measurement_end_time = StringVar()
    timeout_end = StringVar() 
    new_data = StringVar()

    def __init__(self) -> None:
         pass
#############################################################-------Functions-------##################################################################
    def julian_date():
        ''' Coverts UTC to Julian Date'''
        #Striping thing relevant numbers of UTC
        hour_utc = dt.datetime.utcnow().hour
        min_utc = dt.datetime.utcnow().minute
        sec_utc = dt.datetime.utcnow().second
        month_utc = dt.datetime.utcnow().month
        year_utc = dt.datetime.utcnow().year
        day_utc = dt.datetime.utcnow().day
        tsc= dt.datetime.utcnow().microsecond
        #Calculation of JD and MJD
        tA = math.floor((14-month_utc)/12)
        julian_year = (year_utc + 4800 - tA)
        julian_month = (month_utc + (12*tA)-3)
        jdn = (day_utc + math.floor(((153*julian_month+2)/5) + (365*julian_year) + math.floor(julian_year/4) 
                                        - math.floor(julian_year/100) + math.floor(julian_year/400) - 32045))
        FC.mjd = ((jdn + ((hour_utc-12)/24) + (min_utc/1400) + (tsc/86400)) - 2400000.5)
        return FC.mjd
    def display_mdj():
            FC.julian_date()
            messagebox.showinfo("The MJD ", message=FC.julian_date())
    def display_time():
        FC.samples_run = 0
        FC.timeout_min = 60*(FC.user_input_mintues.get())
        FC.timeout_hrs = (FC.user_input_hours.get())/60
        FC.timeout_start = time.time()
        FC.measurement_start_time = (time.asctime(time.localtime(FC.timeout_start)))
        FC.file_string = FC.measurement_start_time + ".txt"
        FC.timeout_end = time.time()
        FC.measurement_end_time = (time.asctime(time.localtime(FC.timeout_end))) 

        return FC.samples_run,FC.timeout_min, FC.timeout_hrs, FC.timeout_start,FC.measurement_start_time, FC.file_string, FC.timeout_end, FC.measurement_end_time
    def file_save():
        FC.julian_date()
        file = FC.output_fileloc
        #temp_file = 'C:\Users\KaiHall\Desktop'
        try:
            with open(file, "a") as textfile:
                textfile.write(f"{FC.samples_run}    {FC.mjd}     {FC.new_data}\n")
                FC.samples_run +=1
                print(f"Sample {FC.samples_run} completed at {FC.measurement_end_time} ")
                time.sleep(FC.seconds_spin.get())
        except FileNotFoundError and TypeError:
            with open('C:/Users/KaiHall/Desktop/temp_file_data.txt', "a") as textfile:
                textfile.write(f"{FC.samples_run}    {FC.mjd}     {FC.new_data}\n")
                FC.samples_run +=1
                print(f"Sample {FC.samples_run} completed at {FC.measurement_end_time} ")
                time.sleep(FC.seconds_spin.get())
        return  
    def time_interval():
        '''Runs the time interval for an alloted number of samples and with n seconds inbetween each sample'''
        # FC.samples_run = 0
        FC.display_time()
        if FC.ch1_signal.get() == 1 and FC.ch2_signal.get() == 2:
            while FC.samples_run < FC.samples_spin.get():
                freq_counter.write('MEAS:TINT? (@1), (@2)')
                sample_data = freq_counter.query_ascii_values('FETCH?', converter='s') 
                sample_Data = str(sample_data[0])
                FC.new_data = sample_Data[:-23]
                FC.file_save() 
        elif FC.ch1_signal.get() == 2 and FC.ch2_signal.get() == 1:
            while FC.samples_run < FC.samples_spin.get():
                freq_counter.write('MEAS:TINT? (@1), (@2)')
                sample_data = freq_counter.query_ascii_values('FETCH?', converter='s') 
                sample_Data = str(sample_data[0])
                FC.new_data = sample_Data[:-23]
                FC.file_save()
        return
    def infinity_samples():
        '''Runs the time interval for a period of time '''
        FC.display_time()
        print(f"The measurements started at {FC.measurement_start_time}")
        print("Here we go...")
        try:
            if FC.timeout_min > 0:
                while time.time() < FC.timeout_start + FC.timeout_min:
                    j = 0
                    freq_counter.write('MEAS:TINT? (@1), (@2)')
                    sample_data = freq_counter.query_ascii_values('FETCH?', converter='s') 
                    time.sleep(1)
                    sample_Data = str(sample_data[0])
                    FC.new_data = sample_Data[:-23]
                    # FC.current_date = FC.mjd
                    FC.timeout_end = time.time()
                    FC.measurement_end_time = (time.asctime(time.localtime(FC.timeout_end))) 
                    FC.file_save()
                    j -= 1
        except:
            print("You need to add some time")
        try:
            if FC.timeout_hrs > 0:
                while time.time() < FC.timeout_start + FC.timeout_hrs:
                    j = 0
                    freq_counter.write('MEAS:TINT? (@1), (@2)')
                    sample_data = freq_counter.query_ascii_values('FETCH?', converter='s') 
                    time.sleep(1)
                    sample_Data = str(sample_data[0])
                    FC.new_data = sample_Data[:-23]
                    hr_timeout_end = time.time()
                    hr_measurement_end_time = (time.asctime(time.localtime(hr_timeout_end)))
                    FC.file_save()
                    j-=1
        except:
            print("You need to add some time")   
        return print(f"Infinite Measurement Completed at {FC.measurement_end_time}!")
    def average_samples(samples_run = 0):
        ''' Calcuates an average of 'n' number of samples'''
        sample_list = []
        print(f"Averaging {FC.avg_spin.get()} samples, stand-by...")
        while samples_run < FC.avg_spin.get():
            freq_counter.write('MEAS:TINT? (@1), (@2)')
            sample_data = freq_counter.query_ascii_values('FETCH?', converter='s') 
            sample_Data = str(sample_data[0])
            time.sleep(1)
            FC.new_data = float(sample_Data[:-23])
            sample_list.append(FC.new_data)
            samples_run +=1
        numbers = 0
        for i in sample_list:
            numbers += i
        print(sample_list)
        try:
            FC.average_sample = numbers/len(sample_list)
            FC.display_time()
            FC.file_save()
            samples_run +=1 
        except ZeroDivisionError:
            print("You cannot average zero readings. Please enter a number of average samples greater than 0!")   
        print(f'Your average reading is: {FC.average_sample}')      
        return 
    def start(): 
        '''Runing a clock measurement basded on user selections'''
        if FC.ch1_signal.get() == FC.ch2_signal.get():
           print("You choose the same single type for two different channels.  Change the Channel Signal type on one channel and try again!") 
        elif FC.measure_mode.get() == 1:
            # if FC.seconds_spin.get() > 0 and FC.samples_spin.get() > 0: FC.time_interval()
            try:
                if FC.seconds_spin.get() > 0 and FC.samples_spin.get() > 0: FC.time_interval()
            except:
                print("I need user to enter numbers for sample reading, both number of samples and the time between them!")          
        elif FC.measure_mode.get() == 2: FC.infinity_samples()
        elif FC.measure_mode.get() == 3: FC.average_samples()
        return print("PyClock App is Finished")
    def choose_file():
        '''Brings up file dictionary for user to select save file location'''
        FC.output_fileloc = filedialog.asksaveasfilename(initialdir="Desktop",defaultextension=("txt"))
    
        return print(f'Your data will be saved at: {FC.output_fileloc}'), FC.output_fileloc   
    def counter_init():
        '''Initializes the counter the the proper settings depending on user selections mode and type of measurment.'''

        def step(value):
            my_progress_bar['value'] += value
        
        progress_label = ttk.Label(mainframe, text="Initialize...")
        progress_label.grid(column=3, row=13, pady=3)
        my_progress_bar = ttk.Progressbar(mainframe, orient=HORIZONTAL, length=100, mode='determinate')
        my_progress_bar.grid(column=3, row=14, sticky='E')

        step(20)

        freq_counter.write('*CLS; *RST') #Clearing and reseting the counter
        sleep: 100
        freq_counter.write('SEN:ROSC:EXT') #Sesnsing the external refference as the 5MHz source
        freq_counter.write('SEN:ROSC:EXT:CEC ONCE') #Checking the external refference as the 5MHz source
        sleep: 100
        freq_counter.write('CONF:TINT (@1),(@2)') # Sets trigger parameters to default values for time interval
        sleep: 100
        freq_counter.write('INP1:IMP 50;:INP2:IMP 50') # Sets the level of input 1 and 2 and impendance to 50 OHMs 
    
        if FC.ch1_signal.get() == 1 and FC.ch2_signal.get() == 2:
            freq_counter.write('INP1:COUP DC; LEV 1.0;:INP2:COUP AC; LEV 0') #Ch.1 Couping to DC, level to 1V
            print("Channel 1 is set to DC")
            print("Channel 2 is set to AC")

        elif FC.ch1_signal.get() == 2 and FC.ch2_signal.get() == 1:
            freq_counter.write('INP1:COUP AC; LEV 0;:INP2:COUP DC; LEV 1.0') #Ch.1 Couplling to AC for Sine Wave, level to 0V
            print("Channel 1 is set to AC")
            print("Channel 2 is set to DC")

        else:
            print("------You didn't select a mode setting for Channel 1 and 2! \nSelect channel pulse and initization again.-----")
            freq_counter.write('*CLS; *RST') 

        step(100)
        progress_label.configure(text="Initialization Completed")
        return print("Initialization is Complete")
##################################################################-------Creating Gui-------#############################################################
ttk.Label(mainframe, text="Channel 1 Signal:").grid(column=0, row=1)
ch1_1pps = ttk.Radiobutton(mainframe, text='1PPS', variable=FC.ch1_signal, value=1)
ch1_1pps.grid(column=1, row=1, sticky="W")
ch1_sine_wave = ttk.Radiobutton(mainframe, text='Sine Wave', variable=FC.ch1_signal, value=2)
ch1_sine_wave.grid(column=2, row=1)

ttk.Label(mainframe, text="Channel 2 Signal:").grid(column=0, row=2)
ch2_2pps = ttk.Radiobutton(mainframe, text='1PPS', variable=FC.ch2_signal, value=1)
ch2_2pps.grid(column=1, row=2, sticky="W")
ch2_sine_wave = ttk.Radiobutton(mainframe, text='Sine Wave', variable=FC.ch2_signal, value=2)
ch2_sine_wave.grid(column=2, row=2)

ttk.Button(mainframe, text="Initialize Counter", command=FC.counter_init).grid(column=0, row=4, pady=4,padx=2, columnspan=2)
ttk.Button(mainframe, text="Display MJD", command=FC.display_mdj).grid(column=1, row=4, pady=4,padx=2, columnspan=2)

ttk.Label(mainframe, text="File To Save Data:").grid(column=0, row=6)
ttk.Button(mainframe, text="Choose File", command=FC.choose_file).grid(column=1, row=6, pady=8, sticky="W")

ttk.Label(mainframe, text="Measurement Mode:").grid(column=0, row=8, pady=7)
single_shot_mode = ttk.Radiobutton(mainframe, text='Single-Shot',variable=FC.measure_mode, value=1)
single_shot_mode.grid(column=1, row=8, pady=7, sticky="W")

ttk.Label(mainframe, text="Seconds\nBetween Readings (0-100):").grid(column=0, row=9, sticky="W")
single_shot_seconds = ttk.Spinbox(mainframe, from_=1, to=100, textvariable=FC.seconds_spin, width=6)  
single_shot_seconds.grid(column=1, row=9, pady=8)
        
ttk.Label(mainframe, text="Samples:").grid(column=0, row=10, sticky="W")
number_samples = ttk.Spinbox(mainframe, from_=1, to=9999999, textvariable=FC.samples_spin, width=6) 
number_samples.grid(column=1, row=10, pady=8)

ttk.Label(mainframe, text="Measurement Mode:").grid(column=0, row=11, pady=7)
infinite_mode = ttk.Radiobutton(mainframe, text='Infinite',variable=FC.measure_mode, value=2)
infinite_mode.grid(column=1, row=11, pady=7, sticky="W")

ttk.Label(mainframe, text="Hours:").grid(column=0, row=12, sticky="E")
user_input_hours = ttk.Spinbox(mainframe, from_=1, to=25, textvariable=FC.user_input_hours, width=6)
user_input_hours.grid(column=1, row=12, pady=8)
        
ttk.Label(mainframe, text="Mintutes:").grid(column=0, row=13, sticky="E")
user_input_mintues = ttk.Spinbox(mainframe, from_=1, to=59, textvariable=FC.user_input_mintues, width=6)
user_input_mintues.grid(column=1, row=13, pady=8)

ttk.Label(mainframe, text="Measurement Mode:").grid(column=0, row=14, pady=10)
average_mode = ttk.Radiobutton(mainframe, text='Averaged', variable=FC.measure_mode, value=3)
average_mode.grid(column=1, row=14, pady=10)

ttk.Label(mainframe, text="Average Samples\n(2-99,000,000):").grid(column=0, row=15, sticky="W")
avg_spin_entry = ttk.Spinbox(mainframe, from_=1, to=100, textvariable=FC.avg_spin, width=6)
avg_spin_entry.grid(column=1, row=15, pady=8)  

ttk.Label(mainframe, textvariable=FC.sample_output).grid(column=3, row=13, columnspan=4)
measure_button = ttk.Button(mainframe, text="Start Reading", command=FC.start).grid(column=3, row=15, pady=3)

# progress_label = ttk.Label(f, text="Progress...").grid(column=1, row=14, pady=3)
# progress_bar = ttk.Progressbar(mainframe, orient=HORIZONTAL, length=150, mode="determinate").grid(column=1, row=15, sticky='E')
#  ttk.Button(mainframe, text="Stop Reading", command=FC.stop).grid(column=1, row=14, pady=3)

root.mainloop()