#include "a.h"

typedef struct
{
	int a;
	int b;
	int c[20];
	/* data */
}struct_a;

int funcTest(int ptr[])
{
	struct_a *data;
	data = (struct_a *)ptr;
	data->a =200;
	//data->b=201;
	//for(int i =0;i<20;i++)
	//{
	//	data->c[i]=i;
	//}
	return 0;
}

int func1(int x, int y){
	return (x+y);
}

void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}