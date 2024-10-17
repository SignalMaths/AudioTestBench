#!/usr/bin/env python3
"""Simple GUI for recording into a WAV file.

There are 3 concurrent activities: GUI, audio callback, file-writing thread.

Neither the GUI nor the audio callback is supposed to block.
Blocking in any of the GUI functions could make the GUI "freeze", blocking in
the audio callback could lead to drop-outs in the recording.
Blocking the file-writing thread for some time is no problem, as long as the
recording can be stopped successfully when it is supposed to.

"""
import tkinter as tk
from tkinter import ttk
from tkinter import *
from datetime import datetime

from DeviceStream import DeviceStream
#from Led import LED
import MenuWindow
import PlotFrame

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import spectrogram
import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class RecGui(tk.Tk):
    stream = None
  
    def __init__(self):
        super().__init__()
        self.manageStream = DeviceStream()
        self.title('SoundSimulation')
        self.geometry('1000x500') 
        
        menubar = Menu(self)
        self.config(menu=menubar)        
        menu1=Menu(menubar,tearoff=False)
        menubar.add_cascade(label='Device Setting',menu=menu1)
        menu1.add_command(label='Source/Device',command=self.on_settings)

        menu3=Menu(menubar,tearoff=False)
        menubar.add_cascade(label='Generation',menu=menu3)
        menu3.add_command(label='Config',command=self.generation_settings)

        self.Info ='NONE'
        self.Info_label = ttk.Label(text=self.Info, font=('Arial', 10),justify="left" )
        self.Info_label.pack(side=tk.BOTTOM,anchor='nw')

        # Frame for simualation status
        #f = ttk.Frame().pack()
        self.rec_button = ttk.Button(self)
        self.rec_button.pack(anchor='w',padx=5, pady=5)

        #self.file_label = ttk.Label(text='<file name>')
        #self.file_label.pack(anchor='w')
#
        #self.angle = 0
        #self.angle_label = ttk.Label(text = 'Angle:')
        #self.angle_label.pack(anchor='w')

        #self.meter = ttk.Progressbar()
        #self.meter['orient'] = 'horizontal'
        #self.meter['mode'] = 'determinate'
        #self.meter['maximum'] = 1.0
        #self.meter.pack(fill='x')
        #self.plot = PlotFrame()
           # 创建 matplotlib 图形和坐标轴
        plot = ttk.Frame().pack()
        self.fig_time, self.ax_time = plt.subplots(figsize=(8, 4))
        self.canvas_time = FigureCanvasTkAgg(self.fig_time, master=plot)
        self.canvas_time.get_tk_widget().pack(anchor='w', expand=1)
        #self.canvas_time.get_tk_widget().grid(row=0, column=0)
##
        self.fig_freq, self.ax_freq = plt.subplots(figsize=(8, 4))
        self.canvas_freq = FigureCanvasTkAgg(self.fig_freq, master=plot)
        self.canvas_freq.get_tk_widget().pack(anchor='w', expand=1)
        #self.canvas_time.get_tk_widget().grid(row=0, column=1)
##
        self.audio_data = None
        self.sample_rate = None


        # We try to open a stream with default settings first, if that doesn't
        # work, the user can manually change the device(s)
        self.protocol('WM_DELETE_WINDOW', self.close_window)
        self.init_buttons()
        #self.update_gui()
    def plot_time_domain(self):
        if self.audio_data is not None:
            self.ax_time.clear()
            self.ax_time.plot(np.linspace(0, len(self.audio_data) / self.sample_rate, num=len(self.audio_data)), self.audio_data)
            self.ax_time.set_title('Time Domain Signal')
            self.ax_time.set_xlabel('Time [s]')
            self.ax_time.set_ylabel('Amplitude')
            self.ax_time.grid()
            self.canvas_time.draw()

    def plot_time_frequency(self):
        if self.audio_data is not None:
            self.ax_freq.clear()
            f, t, Sxx = spectrogram(self.audio_data, self.sample_rate)
            c = self.ax_freq.pcolormesh(t, f, 10 * np.log10(Sxx), shading='gouraud')
            self.ax_freq.set_title('Time-Frequency Representation')
            self.ax_freq.set_ylabel('Frequency [Hz]')
            self.ax_freq.set_xlabel('Time [s]')
            plt.colorbar(c, ax=self.ax_freq, label='Intensity [dB]')
            self.ax_freq.set_ylim(0, self.sample_rate / 2)  # Display only up to Nyquist frequency
            self.canvas_freq.draw()

    def on_settings(self, *args):
        w = MenuWindow.SettingsWindow(self, 'Settings')
        self.manageStream.input_device = w.input_dev_id
        self.manageStream.output_device = w.output_dev_id
        self.manageStream.Info = w.Info

    def generation_settings(self, *args):
        w = MenuWindow.Generate(self, 'Generate')

    def on_rec(self):
        self.recording = True
        filename = 'Sim_'+datetime.now().strftime('%Y_%m_%d_%H_%M_%S')+'.wav'
        self.manageStream.create_stream(self.manageStream.input_device,filename)
        self.rec_button['text'] = 'stop'
        self.rec_button['command'] = self.on_stop
        self.rec_button['state'] = 'normal'
        self.file_label['text'] = 'Recording filename:'+filename

    def on_stop(self, *args):
        self.rec_button['state'] = 'disabled'
        self.recording = False
        self.manageStream.stop_stream(self.manageStream.input_device)
        self.init_buttons()

    def init_buttons(self):
        self.rec_button['text'] = 'Simulation'
        self.rec_button['command'] = self.on_rec
        if self.stream:
            self.rec_button['state'] = 'normal'

    def update_gui(self):
        self.Info_label['text'] = self.manageStream.Info
        #try:
        #    peak = self.metering_q.get_nowait()
        #except queue.Empty:
        #    pass
        #else:
        #    self.meter['value'] = peak
        content = 'DOA(Direction Of Arrival) Angle:'+str(round(self.angle/3.1415926*18)*10)
        self.angle_label['text'] = content
        #self.LedOBJ.LED_Control(int(self.angle/3.1415926*16))
        self.after(500, self.update_gui)

    def close_window(self):
        #if self.recording
        #    self.on_stop()
        self.destroy()

def main():
    
    app = RecGui()
    app.mainloop()

if __name__ == '__main__':
    main()
