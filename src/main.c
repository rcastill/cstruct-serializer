#include <stdio.h>
#include <stdlib.h>
#include "buffer.h"

#define STACK(s)\
    {char *t = s; &t}

int main(int argc, char *argv[])
{
    auto_buffer_t buffer = buffer_create_default();
    buffer_push_int32(buffer, 42);
    buffer_push_string(buffer, "The great number!");

    auto_buffer_t read = buffer_from_data(
        buffer_data(buffer),
        buffer_size(buffer)
    );

    int number;
    char string[256];
    char *s;

    buffer_pop_int32(read, &number);
    buffer_pop_string(read, string, 256);
    //buffer_pop_string(read, &s, BUFFER_ALLOC_STRING);
    
    printf("%d, %s\n", number, string);

    //free(s);
}