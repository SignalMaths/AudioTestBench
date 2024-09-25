#!/usr/bin/env python3
import contextlib
import tkinter as tk
from tkinter import ttk
from tkinter.simpledialog import Dialog
from tkinter import *
import sounddevice as sd
from tkinter import filedialog
from FileThread import FileWriting

class Generate(Dialog):
    def save_file(self,):
        # 弹出保存文件对话框
        file_path = filedialog.asksaveasfilename(title="Save File", filetypes=[("Text files", "*.wav")])
        if(file_path):
            print(file_path)
    def body(self, master):
        ttk.Label(self, text='Sample Rate:').pack(anchor='w')
        sampleRateEntry = tk.Entry(self)
        sampleRateEntry.pack()
        ttk.Label(self, text='Fre Start:').pack(anchor='w')
        FreStartEntry = tk.Entry(self)
        FreStartEntry.pack()
        ttk.Label(self, text='Fre end:').pack(anchor='w')
        FreEndEntry = tk.Entry(self)
        FreEndEntry.pack()
        self.filename ='none'
        SaveButton = tk.Button(self,text='Save',command=self.save_file)
        SaveButton.pack()

    def validate(self):
        # Generate the signal tone
        #self.result = self.device_ids[self.device_list.current()]
        return True

class SettingsWindow(Dialog):
    """Dialog window for choosing sound device."""
    def __init__(self, master, title,type):
        self.value = type
        print(type)
        Dialog.__init__(self, master, title=title)

    def body(self, master):
        self.Info ='NONE'
        self.Info_label = ttk.Label(self,text=self.Info, font=('Arial', 10),justify="left" )
        self.Info_label.pack(side=tk.BOTTOM,anchor='nw')

        ttk.Label(self, text='Select host API:').pack(anchor='w')
        self.hostapi_list = ttk.Combobox(self, state='readonly', width=50)
        self.hostapi_list.pack(anchor='w')
        self.hostapi_list['values'] = [
            hostapi['name'] for hostapi in sd.query_hostapis()]
        # select sound device
        ttk.Label(self, text='Select sound device:').pack(anchor='w')
        self.device_ids = []
        self.device_list = ttk.Combobox(self, state='readonly', width=50)
        self.device_list.pack(anchor='w')
        self.hostapi_list.bind('<<ComboboxSelected>>', self.update_device_list)
        with contextlib.suppress(sd.PortAudioError):
            self.hostapi_list.current(sd.default.hostapi)
            self.hostapi_list.event_generate('<<ComboboxSelected>>')
        #print(self.Infolabel)
        print(self.Info)
    def update_device_list(self, *args):
        hostapi = sd.query_hostapis(self.hostapi_list.current())
        print(hostapi['name'])
        if self.value ==1:
            DeviceType = 'max_input_channels'
            default_device = 'default_input_device'
        else:
            DeviceType = 'max_output_channels'
            default_device = 'default_output_device'
        self.device_ids = [
            idx
            for idx in hostapi['devices']
            if sd.query_devices(idx)[DeviceType] > 0]
        self.device_list['values'] = [
            sd.query_devices(idx)['name'] for idx in self.device_ids]
        default = hostapi[default_device]
        if default >= 0:
            self.device_list.current(self.device_ids.index(default))
        print(self.device_ids)
        self.Info = str(hostapi['name']) + 'device ID:'+str(self.device_ids[self.device_list.current()])
        print(self.Info)
        #print(self.Infolabel)
        self.Info_label['text'] = self.Info

    def validate(self):
        self.result = self.device_ids[self.device_list.current()]
        print(self.device_list.current())
        return True

def main():
    root = tk.Tk()
    root.withdraw()
    app = Generate(root,'Tone Gnerate')

if __name__ == '__main__':
    main()
