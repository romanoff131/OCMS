#include <stdio.h>

#define MAX 11

double autocorrelation(int original[], int shifted[], int length) {
	int k = 0;
	
	for(int i = 0; i < length; i++) {
		if(original[i] == shifted[i]) {
			k++;
		}
	}
	return (double)(k-length/2)/(length/2);
}

void shiftedd(int array[], int shift){
	int a[MAX];
	for(int i = 0; i < MAX; i++) {
		if(i < shift)
			a[i] = array[i+5 - shift];
		else
			a[i] = array[i - shift];
	}
	for(int i = 0; i < MAX; i++)
		array[i] = a[i];
}


int main(){
	int array_x[5] = {};
	int  array_y[5]= {};
  
	int num_x = 0b10011; 
	int num_y = 0b11010;

	for(int i = 0; i < 5; i++) {
		array_x[i] = (num_x >> (4 - i)) & 1;
		array_y[i] = (num_y >> (4 - i)) & 1;
	}

	int original[MAX] = {};
	int shifted[MAX] = {};
  
	// Генерация последовательности Голда.
	for(int i = 0; i < MAX; i++) {
		original[i] = array_x[4] ^ array_y[4];
		shifted[i] = array_x[4] ^ array_y[4];
    
		int sum_x = array_x[0] ^ array_x[2];
		int sum_y = array_y[1] ^ array_y[3];

		for(int j = 4; j >= 0; j--){
			array_x[j] = array_x[j-1];
			array_y[j] = array_y[j-1];
		}
		array_x[0] = sum_x;
		array_y[0] = sum_y; 
	}
	printf("Сдвиг| Бит |Автокорреляция\n");
	for(int shift = 0; shift < MAX; shift++) {
		printf("%5d|", shift);
		for(int i = 0; i < 5; i++) {
			printf("%d", shifted[i]);
		}
		printf("|");
		double autocorr = autocorrelation(original, shifted, 5);
		printf("%+1.1f\n", autocorr-0.5);
		shiftedd(shifted, 1);
	}
	return 0;
}
