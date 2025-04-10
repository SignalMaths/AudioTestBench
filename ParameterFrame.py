#import tkinter as tk
#from tkinter import ttk
#import sounddevice as sd
#
#class ParameterFrame(ttk.LabelFrame):
#    def __init__(self, parent, stream_manager, **kwargs):
#        super().__init__(parent, text="Audio Stream Parameters", padding=10, **kwargs)
#        self.stream_manager = stream_manager
#        
#        # 默认参数
#        self.latency = tk.DoubleVar(value=0.02)
#        self.blocksize = tk.IntVar(value=512)
#        self.samplerate = tk.IntVar(value=48000)
#        
#        self._setup_ui()
#
#    def _setup_ui(self):
#        """初始化参数控件"""
#        # Latency
#        ttk.Label(self, text="Latency (s):").grid(row=0, column=0, sticky="w", padx=5, pady=2)
#        ttk.Entry(self, textvariable=self.latency, width=8).grid(row=0, column=1, sticky="w", padx=5)
#        
#        # Blocksize
#        ttk.Label(self, text="Blocksize:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
#        ttk.Entry(self, textvariable=self.blocksize, width=8).grid(row=1, column=1, sticky="w", padx=5)
#        
#        # Samplerate
#        ttk.Label(self, text="Samplerate:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
#        ttk.Entry(self, textvariable=self.samplerate, width=8).grid(row=2, column=1, sticky="w", padx=5)
#        
#        # Update Button
#        ttk.Button(
#            self,
#            text="Update Parameters",
#            command=self._update_params
#        ).grid(row=3, column=0, columnspan=2, pady=5)
#
#    def _update_params(self):
#        """更新音频流参数"""
#        try:
#            # 更新 stream_manager 的参数
#            self.stream_manager.latency = self.latency.get()
#            self.stream_manager.blocksize = self.blocksize.get()
#            self.stream_manager.samplerate = self.samplerate.get()
#            
#            return True  # 表示成功更新
#        except ValueError as e:
#            return False  # 表示更新失败
#        

import tkinter as tk
from tkinter import ttk
from enum import Enum

class AudioMode(Enum):
    RECORD = "Recording"
    PLAY = "Playback"
    VOIP = "VOIP"
    CUSTOM = "Custom"

class ParameterFrame(ttk.LabelFrame):
    def __init__(self, parent, stream_manager, mode=AudioMode.RECORD, **kwargs):
        super().__init__(parent, text=f"Audio Parameters - {mode.value}", padding=10, **kwargs)
        self.stream_manager = stream_manager
        self.mode = mode
        self._params = {}
        self._setup_ui()

    def _setup_ui(self):
        """根据模式初始化不同的参数控件"""
        # 公共参数
        self._add_param("samplerate", "Samplerate (Hz)", tk.IntVar(value=48000))
        self._add_param("blocksize", "Blocksize", tk.IntVar(value=512))
        
        # 模式特定参数
        if self.mode == AudioMode.RECORD:
            self._add_param("latency", "Input Latency (s)", tk.DoubleVar(value=0.02))
            self._add_param("monitor", "Monitor Input", tk.BooleanVar(value=False))
            
        elif self.mode == AudioMode.PLAY:
            self._add_param("latency", "Output Latency (s)", tk.DoubleVar(value=0.05))
            self._add_param("dither", "Dithering", tk.BooleanVar(value=True))
            
        elif self.mode == AudioMode.VOIP:
            self._add_param("in_latency", "Input Latency (s)", tk.DoubleVar(value=0.02))
            self._add_param("out_latency", "Output Latency (s)", tk.DoubleVar(value=0.05))
            self._add_param("echo_cancel", "Echo Cancellation", tk.BooleanVar(value=True))

        # 更新按钮
        ttk.Button(
            self,
            text="Apply Parameters",
            command=self._update_params
        ).grid(row=len(self._params)+1, column=0, columnspan=2, pady=10)

    def _add_param(self, name, label, var):
        """添加参数控件到界面"""
        row = len(self._params)
        ttk.Label(self, text=label).grid(row=row, column=0, sticky="w", padx=5, pady=2)
        entry = ttk.Entry(self, textvariable=var, width=10)
        entry.grid(row=row, column=1, sticky="w", padx=5)
        self._params[name] = {"var": var, "widget": entry}

    def _update_params(self):
        """更新参数到stream_manager"""
        params = {name: data["var"].get() for name, data in self._params.items()}
        self.stream_manager.update_parameters(self.mode, params)

    def change_mode(self, new_mode):
        """动态切换模式"""
        self.mode = new_mode
        self.config(text=f"Audio Parameters - {new_mode.value}")
        # 清除旧控件
        for child in self.winfo_children():
            child.destroy()
        self._params = {}
        # 重建UI
        self._setup_ui()