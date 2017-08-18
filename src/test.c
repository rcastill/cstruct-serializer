#include <stdint.h>

//! serialize
struct testo
{
    int32_t como;
    int16_t tamos;
};

/*
int testo_serialize(buffer_t buffer, const struct testo *testo)
{
    if (buffer_push_int32(buffer, testo->como) == -1) return -1;
    if (buffer_push_int16(buffer, testo->tamos) == -1) return -1;
    return 0;
}

int testo_deserialize(buffer_t buffer, struct testo *testo)
{
    if (buffer_pop_int32(buffer, &testo->como) == -1) return -1;
    if (buffer_push_int16(buffer, &testo->tamos) == -1) return -1;
    return 0;
}

*/