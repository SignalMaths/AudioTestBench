#!/usr/bin/env python3
"""Simple GUI for recording into a WAV file.

There are 3 concurrent activities: GUI, audio callback, file-writing thread.

Neither the GUI nor the audio callback is supposed to block.
Blocking in any of the GUI functions could make the GUI "freeze", blocking in
the audio callback could lead to drop-outs in the recording.
Blocking the file-writing thread for some time is no problem, as long as the
recording can be stopped successfully when it is supposed to.

"""


import ctypes
from ctypes import cdll, c_int, byref

from ctypes import cdll
from ctypes import *



class AudioProcess:
    print('AudioProcess')
    AudioLib = ctypes.CDLL(r'E:\Project\PythonAudio\Aud_Alog_Project_16ch\build\mylib.so') # so文件路径
    # 定义C函数的参数类型
    AudioLib.libtest.argtypes = [c_void_p]
    AudioLib.Lib_Init.argtypes = [c_void_p]
    AudioLib.Lib_Process.argtypes = None
 
    # 定义C函数的返回类型
    AudioLib.libtest.restype = None
    AudioLib.Lib_Init.restype = ctypes.c_void_p
    AudioLib.Lib_Process.restype = c_int
 
    # 创建一个字符串的字节表示，并转换为void*
    message_bytes = b"Hello from C!"
    void_message = cast(message_bytes, c_void_p)
    AudioLib.libtest(void_message)
    Vc_ptr = AudioLib.Lib_Init(void_message)
    
    para = c_void_p(None)
    Vc_ptr = AudioLib.Lib_Init(byref(para))
    #AudioLib.Lib_Init(void_message)
    #so2.Lib_Process(None)
    
    def __init__(self, value=None):
        self.data = value
 
    def operation(self, value):
        self.AudioLib.Lib_Process()
 
    def get_value(self):
        return self.data
 
    def greet(self):
        print(f"Hello, my value is {self.data}!")
def main():
    print('main')
    AudioProcess()


if __name__ == '__main__':
    main()

    




