import ctypes
from ctypes import cdll, c_int, byref

from ctypes import cdll
from ctypes import *

# 
## 加载共享库
#lib = cdll.LoadLibrary('./libexample.so')

#dllpath=r'E:\Project\PythonAudio\Test\dll.dll'
#dll=CDLL(dllpath)
## 创建两个整数变量
#a = c_int(5)
#b = c_int(10)
#dll.funcTest.argtypes =[ctypes.POINTER(ctypes.c_int)]
#dll.swap.argtypes = [c_int, c_int]
## 定义swap函数的返回类型
#dll.swap.restype = None
#dll.swap(a, b)
#print(a.value, b.value)  # 输出应该是10 5


so = ctypes.CDLL(r'E:\Project\PythonAudio\Test\test.so') # so文件路径
for i in range(10):
    for j in range(5):
        print(i,j)
        
so.funcTest.argtypes = [c_int*22]
so.funcTest.restype = None
IntArray10 = c_int*22
my_int = IntArray10()
for i in range(0,22):
    my_int[i] =i
    print(my_int[i])
C_funcTest = so.funcTest
#so.funcTest(pointer(my_int))
C_funcTest(my_int)
print('================')
for i in range(0,22):
    print(my_int[i])
#print(my_int(1))
#a = so.func1(1, 2)
#print(a)

# 定义swap函数的参数类型
so.swap.argtypes = [POINTER(c_int), POINTER(c_int)]
 
# 定义swap函数的返回类型
so.swap.restype = None
 
a = c_int(5)
b = c_int(10)
# 调用swap函数
so.swap(pointer(a),pointer(b))
 
# 打印结果
print(a.value, b.value)  # 输出应该是10 5



