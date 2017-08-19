# CSTRUCT-SERIALIZER

This project intends to develop a minimalistic serializer for struct in C.

## How does it achieve it?
This serializer writes each attribute of a *marked* struct into a byte array. For making this process easier, a small library called `buffer` was developed.
This library provides functions to push data to a byte array; in order to make it simpler, a buffer **always** owns the data, this means, if the user wants to write to it, he/she has to copy it.

## Expectations
`buffer` library aside, a **precompiler** is being developed. Its task is to detect all *marked* structs within a C file and generate C valid sources that use the `buffer` library in order to serialize the struct.

## Example
A target C source would be:
```c
//! serialize
struct nice_struct
{
    int32_t data1;
    int16_t data2;
    char    data3;
};

struct bad_struct
{
    int8_t data1;
    char   data2[];
};
```
In this case, the precompiler would parse `nice_struct` only, since `bad_struct` is not *marked*.

...

### Work under process!