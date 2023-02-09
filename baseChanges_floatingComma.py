"""This program consist of four main functions and some auxiliary ones

The first one changes numbers from base 10 to base N.
The second one changes numbers from base N to base 10.
The third one changes numbers from base N to base M.
The fourth one changes numbers in base N to their floating comma representation.
"""
from math import floor


# Auxiliary function. Receives an integer in base 10 and returns it in base N.
def whole_part(integer, base=2):
    digits_backwards = []

    """
    Let a and b be integers. The euclidean division of a by b yields a=b·q_1+r_1. We divide q_1 by b and obtain
    a=b·(b·q_2+r_2)+r_1=b^2·q_2+b·r_2+r_1. We repeat this process until some q_n is smaller than b, and obtain
    a=b^n·q_n+b^(n-1)·r_n+b^(n-2)·r_(n-1)+...+b·r_2+r_1, with q_n<b and r_i<b for all i=1,...,n.
    Therefore, a=(q_n,r_n,r_(n_1),...,r_2,r_1)_b.
    
    This loop implements the algorithm described above.
    """
    while integer >= base:
        digits_backwards.append(integer % base)
        print(integer)
        integer //= base

    digits_backwards.append(integer)

    res = ""
    for i in range(len(digits_backwards)):
        res += str(digits_backwards[-(i + 1)])

    return res


# Auxiliary function. Receives a <1 number in the format 0.abcd... in base 10 and returns it in base N
def decimal_part(number, base=2):
    digits = []

    """
    Let 0.abcd... be the number's representation in base N. If we multiply it by N we get a.bcde... Since
    (N·x)_10=(N·x)_N, we can use this to know the number's representation in base N using the floor function to 
    extract the value of a.
    
    At each iteration of the loop, we substract the whole part of the number. The process follows this scheme:
    
    0.abcd... -> a.bcde -> 0.bcde -> b.cdef -> 0.cdef -> c.defg -> 0.defg -> ...     
    """
    digit_count = 1
    while number != 0 and digit_count <= 15:  # Python floats have 15 decimal places at most.
        digit_count += 1
        number *= base
        int_part = floor(number)
        digits.append(int_part)
        number -= int_part

    res = "".join([str(i) for i in digits])

    return res


# Receives a number in base 10 and the number N. Returns the original number in base N.
def ten_to_n(number, base=2):
    int_part_10 = floor(number)
    dec_part_10 = number - int_part_10

    int_part = whole_part(int_part_10, base)
    dec_part = decimal_part(dec_part_10, base)

    return float(int_part + "." + dec_part)


# Receives a number in base N and the number N itself. Returns the original number in base 10.
def n_to_ten(number, base=2):
    string = str(number)

    whole = []
    decimal = []
    point_yet = False

    # This loop separates the whole part and the decimal part of the number and puts it in two different lists.
    for char in string:
        if char == ".":
            point_yet = True
        elif not point_yet:
            whole.append(int(char))
        else:
            decimal.append(int(char))

    res = 0

    # We now read the number digit to digit and sum the corresponding value.
    for i in range(len(whole)):
        res += base ** i * whole[-(i + 1)]

    for i in range(len(decimal)):
        res += base ** (-(i + 1)) * decimal[i]

    return res


# Receives a number in base N and the numbers N and M. Returns the original number in base M.
def n_to_m(number, base_in, base_out):
    return ten_to_n(n_to_ten(number, base_in), base_out)


# Receives a nonzero number in base N and the number N. Returns a tuple with the sign, mantissa, base and exponent of
# the number, in that order.

def floating_comma(number, base=2):
    sign = None

    if number >= 0:
        sign = 0
    else:
        number = -number
        sign = 1

    number = n_to_ten(number, base)

    exponent = 0
    if number >= 1:
        while number >= 1:
            number /= base
            exponent += 1
    else:
        while number < 1:
            exponent -= 1
            number *= base
        exponent += 1
        number /= base

    return sign, ten_to_n(number), base, exponent
