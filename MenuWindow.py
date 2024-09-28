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
    #def __init__(self, master, title):
    #    Dialog.__init__(self, master, title=title)

    def body(self, master):

        # input device Frame
        self.init =0
        self.FrameInputDevice = Frame(self)
        self.FrameInputDevice.pack(anchor='w')
        self.Info ='NONE'
        ttk.Label(self.FrameInputDevice, text='Device Input:\nSelect host API:').pack(anchor='w')
        self.input_hostapi_list = ttk.Combobox(self.FrameInputDevice, state='readonly', width=50)
        self.input_hostapi_list.pack(anchor='w')
        self.input_hostapi_list['values'] = [
            hostapi['name'] for hostapi in sd.query_hostapis()]

        # select sound device
        ttk.Label(self.FrameInputDevice, text='Select input device:').pack(anchor='w')
        self.device_input_ids = []
        self.device_input_list = ttk.Combobox(self.FrameInputDevice, state='readonly', width=50)
        self.device_input_list.pack(anchor='w')
        self.input_hostapi_list.bind('<<ComboboxSelected>>', self.update_input_hostapis_list)
        with contextlib.suppress(sd.PortAudioError):
            self.input_hostapi_list.current(sd.default.hostapi)
            self.input_hostapi_list.event_generate('<<ComboboxSelected>>')
        self.device_input_list.bind('<<ComboboxSelected>>', self.update_input_dev)

        # output device for configure.
        self.FrameDeviceOut = Frame(self)
        self.FrameDeviceOut.pack(anchor='w')
        ttk.Label(self.FrameDeviceOut, text='Device Output:\nSelect host API:').pack(anchor='w')
        self.out_hostapi_list = ttk.Combobox(self.FrameDeviceOut, state='readonly', width=50)
        self.out_hostapi_list.pack(anchor='w')
        self.out_hostapi_list['values'] = [
            hostapi['name'] for hostapi in sd.query_hostapis()]
        # select sound device
        ttk.Label(self.FrameDeviceOut, text='Select output device:').pack(anchor='w')
        self.device_ids = []
        self.device_list = ttk.Combobox(self.FrameDeviceOut, state='readonly', width=50)
        self.device_list.pack(anchor='w')
        self.out_hostapi_list.bind('<<ComboboxSelected>>', self.update_Out_hostapi_list)
        #self.device_list.bind('<<ComboboxSelected>>', self.update_Outdevice_list)
        with contextlib.suppress(sd.PortAudioError):
            self.out_hostapi_list.current(sd.default.hostapi)
            self.out_hostapi_list.event_generate('<<ComboboxSelected>>')
        self.device_list.bind('<<ComboboxSelected>>', self.update_output_dev)

        self.FrameInfo = Frame(self)
        self.FrameInfo.pack(anchor='w')
        self.Info_label = ttk.Label(self.FrameInfo,text=self.Info, font=('Arial', 10),justify="left" )
        self.Info_label.pack(anchor='w')
        self.init =1
        self.update_gui()

    def update_input_hostapis_list(self, *args):
        self.input_shostapi = sd.query_hostapis(self.input_hostapi_list.current())
        DeviceType = 'max_input_channels'
        default_device = 'default_input_device'
        self.device_input_ids = [
            idx
            for idx in self.input_shostapi['devices']
            if sd.query_devices(idx)[DeviceType] > 0]
        self.device_input_list['values'] = [
            sd.query_devices(idx)['name'] for idx in self.device_input_ids]
        default = self.input_shostapi[default_device]
        if default >= 0:
            self.device_input_list.current(self.device_input_ids.index(default))
        self.input_dev_id = self.device_input_ids[self.device_input_list.current()]
        self.input_dev=sd.query_devices(self.input_dev_id)
        if(self.init ==1):
            self.update_gui()

    def update_input_dev(self, *args):
        self.input_shostapi = sd.query_hostapis(self.input_hostapi_list.current())
        self.input_dev_id = self.device_input_list.current()
        self.input_dev=sd.query_devices(self.device_input_ids[self.input_dev_id])
        if(self.init ==1):
            self.update_gui()

    def update_Out_hostapi_list(self, *args):
        self.out_hostapi = sd.query_hostapis(self.out_hostapi_list.current())
        DeviceType = 'max_output_channels'
        default_device = 'default_output_device'
        self.device_ids = [
            idx
            for idx in self.out_hostapi['devices']
            if sd.query_devices(idx)[DeviceType] > 0]
        self.device_list['values'] = [
            sd.query_devices(idx)['name'] for idx in self.device_ids]
        default = self.out_hostapi[default_device]
        if default >= 0:
            self.device_list.current(self.device_ids.index(default))
        self.output_dev_id = self.device_ids[self.device_list.current()]
        self.output_dev=sd.query_devices(self.output_dev_id)
        if(self.init ==1):
            self.update_gui()
        
    def update_output_dev(self, *args):
        self.output_dev_id = self.device_list.current()
        self.output_dev=sd.query_devices(self.device_ids[self.output_dev_id])
        if(self.init ==1):
            self.update_gui()

    def update_gui(self):
        
        str_input = 'Input device:\n' +self.input_shostapi['name']+ '\t'+self.input_dev['name']
        srt_output = 'Output device:\n' +self.out_hostapi['name']+ '\t'+self.output_dev['name']
        self.Info = str_input+ '\n'+srt_output
        #print('update gui ==================')
        #print('>>>>>>>>>>>input device')
        #print(self.input_shostapi['name'])
        #print(self.device_input_ids)
        #print(self.input_dev['name'])
        #print('>>>>>>>>>>>output device')
        #print(self.out_hostapi['name'])
        #print(self.device_ids)
        #print(self.output_dev['name'])
        ##print(self.Info)
        #print('update gui>>>>>>>>>>>>>>>>>')
        self.Info_label['text'] = self.Info
        #self.after(100, self.update_gui)


    def validate(self):
        self.result = self.device_ids[self.device_list.current()]
        print(self.device_list.current())
        return True

def main():
    root = tk.Tk()
    root.withdraw()
    #app = Generate(root,'Tone Gnerate')
    testMenu = SettingsWindow(root,'test')

if __name__ == '__main__':
    main()
