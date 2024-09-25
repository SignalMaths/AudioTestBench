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
    def body(self, master):
        self.frame = ttk.Frame(self)
        self.frame.pack()
        radio_value = tk.StringVar()
        radio1 = ttk.Radiobutton(self.frame, text="Device",variable=radio_value, value="1", command=self.createframe01).grid(row=0, column=0, padx=10, pady=10)
        radio2 = ttk.Radiobutton(self.frame, text="File",variable=radio_value, value="2", command=self.createframe02).grid(row=0, column=1, padx=10, pady=10)
        self.frame2 = ttk.Frame(self)
        self.frame2.pack()
        self.setup_frame01()
        self.frame3 = ttk.Frame(self)
        self.frame3.pack(anchor='w')
        self.label = ttk.Label(self.frame3, text='Default info').pack(anchor='e')

    def update_device_list(self, *args):
        hostapi = sd.query_hostapis(self.hostapi_list.current())
        self.device_ids = [
            idx
            for idx in hostapi['devices']
            if sd.query_devices(idx)['max_input_channels'] > 0]
        self.device_list['values'] = [
            sd.query_devices(idx)['name'] for idx in self.device_ids]
        default = hostapi['default_input_device']
        if default >= 0:
            self.device_list.current(self.device_ids.index(default))

    def validate(self):
        self.result = self.device_ids[self.device_list.current()]
        return True
    
    def setup_frame01(self):
        self.frame01 = Frame(self.frame2, relief="groove")
        #self.frame01.place(relwidth=0.84, relheight=0.82, relx=0.16, rely=0.18)
        self.frame01.pack()
        ttk.Label(self.frame01, text='Select host API:').pack(anchor='w')
        self.hostapi_list = ttk.Combobox(self.frame01, state='readonly', width=50)
        self.hostapi_list.pack()
        self.hostapi_list['values'] = [
            hostapi['name'] for hostapi in sd.query_hostapis()]
        # select sound device
        ttk.Label(self.frame01, text='Select sound device:').pack(anchor='w')
        self.device_ids = []
        self.device_list = ttk.Combobox(self.frame01, state='readonly', width=50)
        self.device_list.pack()
        self.hostapi_list.bind('<<ComboboxSelected>>', self.update_device_list)
        with contextlib.suppress(sd.PortAudioError):
            self.hostapi_list.current(sd.default.hostapi)
            self.hostapi_list.event_generate('<<ComboboxSelected>>')

    def setup_frame02(self):
        print()

    def createframe01(self):
        try:
            self.frame01.destroy()
        except:
            pass
        finally:
            try:
                self.frame02.destroy()
            except:
                pass
            finally:
                self.setup_frame01()

    def createframe02(self):
        try:
            self.frame01.destroy()
        except:
            pass
        finally:
            try:
                self.frame02.destroy()
            except:
                pass
            finally:
                self.setup_frame02()


class OutSettingsWindow(Dialog):
    """Dialog window for choosing sound device."""
    def body(self, master):
        self.frame = ttk.Frame(self)
        self.frame.pack()
        radio_value = tk.StringVar()
        radio1 = ttk.Radiobutton(self.frame, text="Device",variable=radio_value, value="1", command=self.createframe01).grid(row=0, column=0, padx=10, pady=10)
        radio2 = ttk.Radiobutton(self.frame, text="File",variable=radio_value, value="2", command=self.createframe02).grid(row=0, column=1, padx=10, pady=10)
        self.frame2 = ttk.Frame(self)
        self.frame2.pack()
        self.setup_frame01()
        self.frame3 = ttk.Frame(self)
        self.frame3.pack(anchor='w')
        self.label = ttk.Label(self.frame3, text='Default info').pack(anchor='e')

    def update_device_list(self, *args):
        hostapi = sd.query_hostapis(self.hostapi_list.current())
        self.device_ids = [
            idx
            for idx in hostapi['devices']
            if sd.query_devices(idx)['max_output_channels'] > 0]
        self.device_list['values'] = [
            sd.query_devices(idx)['name'] for idx in self.device_ids]
        default = hostapi['default_output_device']
        if default >= 0:
            self.device_list.current(self.device_ids.index(default))

    def validate(self):
        self.result = self.device_ids[self.device_list.current()]
        return True
    
    def setup_frame01(self):
        self.frame01 = Frame(self.frame2, relief="groove")
        #self.frame01.place(relwidth=0.84, relheight=0.82, relx=0.16, rely=0.18)
        self.frame01.pack()
        ttk.Label(self.frame01, text='Select host API:').pack(anchor='w')
        self.hostapi_list = ttk.Combobox(self.frame01, state='readonly', width=50)
        self.hostapi_list.pack()
        self.hostapi_list['values'] = [
            hostapi['name'] for hostapi in sd.query_hostapis()]
        # select sound device
        ttk.Label(self.frame01, text='Select sound device:').pack(anchor='w')
        self.device_ids = []
        self.device_list = ttk.Combobox(self.frame01, state='readonly', width=50)
        self.device_list.pack()
        self.hostapi_list.bind('<<ComboboxSelected>>', self.update_device_list)
        with contextlib.suppress(sd.PortAudioError):
            self.hostapi_list.current(sd.default.hostapi)
            self.hostapi_list.event_generate('<<ComboboxSelected>>')

    def setup_frame02(self):
        print()

    def createframe01(self):
        try:
            self.frame01.destroy()
        except:
            pass
        finally:
            try:
                self.frame02.destroy()
            except:
                pass
            finally:
                self.setup_frame01()

    def createframe02(self):
        try:
            self.frame01.destroy()
        except:
            pass
        finally:
            try:
                self.frame02.destroy()
            except:
                pass
            finally:
                self.setup_frame02()

def main():
    root = tk.Tk()
    root.withdraw()
    app = Generate(root,'Tone Gnerate')

if __name__ == '__main__':
    main()
