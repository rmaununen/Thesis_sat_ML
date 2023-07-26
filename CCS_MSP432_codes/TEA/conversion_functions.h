#include <stdint.h>


#ifndef FLOAT_TO_STR_H
#define FLOAT_TO_STR_H

#define MAX_FLOAT_STR_LEN 32

void float_to_str(char* buf, uint32_t bufsize, uint32_t num_decimal_places, float f);

#endif /* FLOAT_TO_STR_H */



#ifndef STRING_TO_FLOAT_H
#define STRING_TO_FLOAT_H

float string_to_float(const char* str);

#endif // STRING_TO_FLOAT_H
