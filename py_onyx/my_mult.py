""" An effective way to multiply 2 huge non-negative integers 

Convert a multipication to a series of bit-shift and sum-up.
The max number of bit-shift to calculate a * b is log2(a) (bit-shift a)

For example:
a = 0101, b = 0011
(bit 0 of a) 1: b * 1 * 1 = 0011
(bit 1 of a) 0: b * 2 * 0 = 0000
(bit 2 of a) 1: b * 4 * 1 = 1100
(bit 3 of a) 0: b * 8 * 0 = 0000
sum:                        1111

So 0101 * 0011 = 1111
"""


def my_mult(a: int, b: int) -> int:
    """ Multiply 2 non-negative integers by bit shift """
    # arguments validation
    if not isinstance(a, int) or not isinstance(b, int):
        raise TypeError ('Arguments must be integers')
    elif a < 0 or b < 0:
        raise ValueError ('Arguments must be non-negative')
    # handling special cases - no need to do calculation in those cases
    elif a == 0 or b == 0:
        return 0
    elif a == 1:
        return b
    elif b == 1:
        return a
    
    sum = 0
    while a:  # loop if a is not 0
        if a & 1:  # sum-up if the least-significant bit of a is 1
            sum += b

        # shift a and b by 1 bit for next round
        a >>= 1
        b <<= 1

    return sum


def main():
    print(my_mult(8, 1))


if __name__ == '__main__':
    main()
