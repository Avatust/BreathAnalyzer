#ifndef RANGE_MAPPING_H
#define RANGE_MAPPING_H

#include <math.h>

float scale(
        float input_value,
        float min_in, float max_in,
        float min_out, float max_out,
        float exponent = 1
        );

class MapRange {
public:
    MapRange(
            float min_in, float max_in,
            float min_out, float max_out,
            float exponent = 0);

    float operator()(float input_value) const;

private:
    float min_in, max_in, min_out, range_out, exponent;
};

#endif // RANGE_MAPPING_H
