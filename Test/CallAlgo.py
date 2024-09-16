from AlgoProcess import AlgoProcess


## 导入class_definition模块中的MyClass类
#from class_definition import MyClass
# 
## 创建MyClass的实例
#my_instance = MyClass(10)
# 
## 调用MyClass的方法
#my_instance.display_value()

print("main")

class B:
    def __init__(self):
        self.instance = AlgoProcess()
        self.instance.process()
        print("Class B initialized with an instance of class A.")
TEST = B()

def main():
    TEST = B()
    print('main')
    
    #print(TestObj.status)


