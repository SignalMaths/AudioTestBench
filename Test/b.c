/* b.c */
#include "a.h"
#include "b.h"
int func2(int x, int y){
	return func1(x,y); // 此处对func1有调用
}

static int func3(int x, int y){ // 定义静态函数，这样外部无法调用
	return (x-y);
}
