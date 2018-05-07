#include "range_mapping.h"

float scale(
        float input_value,
        float min_in, float max_in,
        float min_out, float max_out,
        float exponent
        )
{
    // constrain input
    input_value = input_value < min_in ? min_in : input_value;
    input_value = max_in < input_value ? max_in : input_value;
    exponent = exponent < 0 ? 0 : exponent;

    float normalized =
            (input_value - min_in)
               / (max_in - min_in);

    return (max_out - min_out) * pow(normalized, exponent) + min_out;
}


MapRange::MapRange(
        float min_in, float max_in,
        float min_out, float max_out,
        float exponent)
        :
        min_in(min_in), max_in(max_in),
        min_out(min_out), range_out(max_out - min_out),
        exponent(exponent < 0 ? 0 : exponent)
{
}

float MapRange::operator()(float input_value) const
{
    // constrain input
    input_value = input_value < min_in ? min_in : input_value;
    input_value = max_in < input_value ? max_in : input_value;

    float normalized =
            (input_value - min_in)
               / (max_in - min_in);

    return pow(normalized, exponent) * range_out + min_out;
}
