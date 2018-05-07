#ifndef CIRCULAR_ARRAY_H
#define CIRCULAR_ARRAY_H

using index_type = unsigned int;

template<typename ARR_TYPE, index_type ARR_SIZE>
class CircularArray {
public:
    // CircularArray(arr_type (&array)[ARR_SIZE], int head = 0);
    CircularArray()
        : array{}, head(0)
    {
    }

    ARR_TYPE getRecentValue(index_type NthLast = 0) const // 0th is the most recent one
    {
        return array[(head + ARR_SIZE - NthLast) % ARR_SIZE];
    }

    float getAverage() const
    {
        float sum = 0;
        for (index_type i = 0; i < ARR_SIZE; ++i)
            sum += getRecentValue(i);

        return sum/ARR_SIZE;
    }

    void pushValue(ARR_TYPE value)
    {
        head = (head + 1) % ARR_SIZE;
        array[head] = value;
    }


private:
    ARR_TYPE array[ARR_SIZE];
    index_type head;
};

#endif
