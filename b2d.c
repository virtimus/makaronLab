
#include <stdio.h>
#include <stdint.h>

#define isize 64

int c[isize];

char ch[isize+1];

void fast_d2b(uint64_t x, int * c) {
    int i;
    for(i=0;i<isize;i++)
        *(c++) = (x >> i) & 0x1;
};

void fast_d2s(uint64_t x, char* c) {
    int i;
    int offset = 48; //asc('0')
    for(i=0;i<isize;i++)
        *(c++) = 48 + ((x >> i) & 0x1);
    *(c++) = 0;
};

void fast_b2d(uint64_t *n, int* c){
    int i = isize;   
    *n = 0;   
    while(i--) {
        *n <<= 1;
        *n += *(c+i);
    }
};

void fast_s2d(char* c, uint64_t *n){
    int i = isize;   
    *n = 0;   
    while(i--) {
        *n <<= 1;
        int p = (*(c+i)) - 48;
        //printf("b%d",p);
        *n += p;
    }
};

main(){
    int k;   
    uint64_t x,  y,  yc;
    printf("\nEnter an integer number");   
    printf(" smaller than xxx : ");   
    scanf("%lu", &x);   
    printf("\nCalling fast_d2b for ");   
    printf("decimal to binary conversion :\n");   
    fast_d2b(x, c);   
    printf("   Bin # =");   
    for (k=isize-1; k>=0; k--)      
        printf(" %d",c[k]);   
    printf("\n\nCalling fast_b2d for ");  
    printf("binary to decimal conversion :\n");   
    fast_b2d(&y, c);   
    printf("   Dec # = %lu\n", y); 
    printf("\nCalling fast_d2s for ");   
    printf("decimal to binary conversion :\n");   
    fast_d2s(y, ch);   
    printf("   Bin # = %s",ch);

    printf("\n\nCalling fast_s2d for ");  
    printf("binary to decimal conversion :\n");   
    fast_s2d(ch,&yc); 
    printf("   Dec # = %lu\n", yc); 


    return 0;
}