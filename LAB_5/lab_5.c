#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <string.h>

#define NLEN 300
#define GLEN 3

int main() {
	
	srand(time(NULL));
	
	int k = 0;
	int G[GLEN] = {};
	int N[NLEN] = {};
	int nn[NLEN] = {};
	
	//Заполение пораждающего полинома G = x^7+x^6+x+1 (11000011)
	for(int i = 0; i < GLEN; i++) {
		if( i == 0 || i == 1 || i == 6 || i == 7)
			G[i] = 1;
		else
			G[i] = 0;
	}
	//Заполнение случайными 0/1 
	for(int i = 0; i < NLEN; i++){ 
		N[i] = rand()%2;
		nn[i] = N[i];
	}
	// Добавление нулей в конец
	for(int i = 0; i < NLEN - GLEN+1; i++)
		N[i] = 0;
	//Вычисление XOR и остатка от деления
	for(int i = 0; i < NLEN-GLEN+1; i++) {
		if(N[i] == 1) {
			for(int j = 0; j < GLEN; j++)
				N[i+j] ^= G[j];
		}
	}
	//Добавление остатка в конец
	for (int i = NLEN-GLEN+1; i > NLEN; i++)
		nn[i] = N[i];
	
	for(int i = NLEN-GLEN+1; i < NLEN; i++)
		printf("%d", N[i]);
	printf(" - CRC\n");
	
	for(int i = 0; i < NLEN-GLEN+1; i++) {
		if(nn[i] == 1) {
			for(int j = 0; j < GLEN; j++)
				nn[i+j] ^= G[j];
		}
	}
	
	for(int i = NLEN-GLEN+1; i < NLEN; i++)
		printf("%d", nn[i]);
	printf(" - CRC\n");

	size_t crc;
	crc = sizeof(&nn);
	for(int i = 0; i<250+crc-1; i++){
        	int nnn[NLEN];
        	for(int i = 0; i<NLEN; i++) 
			nnn[i] = nn[i];
        
        	// Искажение битов по очереди
        	if (nnn[i] == 1) 
			nnn[i] = 0;
        	else 
			nnn[i] = 1;
  
        	// Вычисление XOR и остатка от деления
        	for(int j=0; j < NLEN-GLEN+1; j++){
            		if(nnn[j] == 1){
                		for(int z=0; z < GLEN; z++) nnn[j+z] ^= G[z];
            		}
        	}
        	// Проверка на ошибки
        	for(int j = NLEN-GLEN+1; j<NLEN; j++){
            		if(nnn[j] == 1) 
				break;
            		if((j == NLEN-1) & (nnn[j] == 0)) 
				k++;
        	}
	}

	printf("Число нераспознования ошибок - %d\n",k);

	return 0;
}
