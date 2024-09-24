import tkinter as tk
from tkinter import ttk
 
class SettingsWindow(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.title("Settings")
        self.geometry("300x200")
        self.controller = controller
 
        # 设置变量，用于跟踪选中的radiobutton
        self.selected_theme = tk.StringVar()
 
        # 创建两个radiobuttons，并将它们关联到同一个变量
        self.radio_light = ttk.Radiobutton(self, text="Light Theme", variable=self.selected_theme, value="light")
        self.radio_light.pack()
        self.radio_dark = ttk.Radiobutton(self, text="Dark Theme", variable=self.selected_theme, value="dark")
        self.radio_dark.pack()
 
        # 创建一个按钮，当点击时，根据选中的radiobutton改变主题
        self.button_apply = ttk.Button(self, text="Apply", command=self.apply_settings)
        self.button_apply.pack()
 
    def apply_settings(self):
        theme = self.selected_theme.get()
        if theme == "light":
            self.controller.set_theme("light")
        elif theme == "dark":
            self.controller.set_theme("dark")
        self.destroy()
 
# 假设Controller类有set_theme方法用于改变主题
class Controller:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Application")
        self.theme = "light"
        
 
    def set_theme(self, theme):
        self.theme = theme
        if theme == "light":
            self.root.configure(background="white")
        elif theme == "dark":
            self.root.configure(background="black")
 
    def show_settings(self):
        SettingsWindow(self.root, self)
 
    def run(self):
        self.root.mainloop()
 
# 应用示例
if __name__ == "__main__":
    app = Controller()
    theme ='light'
    app.show_settings()
    app.run()

#import ctypes
#from ctypes import cdll, c_int, byref
#
#from ctypes import cdll
#from ctypes import *
#
## 
### 加载共享库
##lib = cdll.LoadLibrary('./libexample.so')
#
##dllpath=r'E:\Project\PythonAudio\Test\dll.dll'
##dll=CDLL(dllpath)
### 创建两个整数变量
##a = c_int(5)
##b = c_int(10)
##dll.funcTest.argtypes =[ctypes.POINTER(ctypes.c_int)]
##dll.swap.argtypes = [c_int, c_int]
### 定义swap函数的返回类型
##dll.swap.restype = None
##dll.swap(a, b)
##print(a.value, b.value)  # 输出应该是10 5
#
#
#so = ctypes.CDLL(r'E:\Project\PythonAudio\Test\test.so') # so文件路径
#for i in range(10):
#    for j in range(5):
#        print(i,j)
#        
#so.funcTest.argtypes = [c_int*22]
#so.funcTest.restype = None
#IntArray10 = c_int*22
#my_int = IntArray10()
#for i in range(0,22):
#    my_int[i] =i
#    print(my_int[i])
#C_funcTest = so.funcTest
##so.funcTest(pointer(my_int))
#C_funcTest(my_int)
#print('================')
#for i in range(0,22):
#    print(my_int[i])
##print(my_int(1))
##a = so.func1(1, 2)
##print(a)
#
## 定义swap函数的参数类型
#so.swap.argtypes = [POINTER(c_int), POINTER(c_int)]
# 
## 定义swap函数的返回类型
#so.swap.restype = None
# 
#a = c_int(5)
#b = c_int(10)
## 调用swap函数
#so.swap(pointer(a),pointer(b))
# 
## 打印结果
#print(a.value, b.value)  # 输出应该是10 5



