#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void ignore_me_init_buffering() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

int main(void)
{
    ignore_me_init_buffering();
    char buff[15];
    int pass = 0;

    puts("Enter the password:\n");
    gets(buff);

    if(strcmp(buff, "thegeekstuff"))
    {
        puts("Wrong Password \n");
    }
    else
    {
        puts("Correct Password \n");
        pass = 1;
    }

    if(pass)
    {
       /* Now Give root or admin rights to user*/
        puts("Root privileges given to the user \n");
        FILE *f = fopen("flag", "r");
        char *str = (char*)malloc(sizeof(char) * 100);
        memset(str, 0, 100);
        fscanf(f, "%s", str);
        puts(str);
    }

    return 0;
}

