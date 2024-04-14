import sys
import collections

from .products import digits
from .sum_of_two import difficulty_of_sum
from .differences import difficulty_of_difference

N = int((sys.argv[1:2] or [123_456])[0])

MAX = int((sys.argv[2:3] or [5000])[0])

def fractions(n = N):
    for i in range(1, MAX - n + 1):
        yield n * i, i


def difficulty_of_long_division(
    numerator: int,
    denominator: int,
    radix: int = 10,
    cache_size: int = 3,
    ):

    assert numerator % denominator == 0, f'{numerator=}, {denominator=}.  Division with remainder not implemented yet'


    numerator_digits = reversed(list(digits(numerator, radix)))

    buffer = 0
    remainder = 0

    retval = 0

    quotient = 0

    for digit in numerator_digits:

        buffer *= radix
        quotient *= radix
        remainder *= radix

        buffer += digit

        if buffer < denominator:
            # compare sizes
            retval += 1
            continue

        multiplier = 0

        while denominator * (multiplier + 1) <= buffer:
            retval += difficulty_of_sum((denominator * multiplier, denominator), radix, cache_size)
            
            # compare sizes
            retval + 1
            
            multiplier += 1

        print(f'{buffer=}, {multiplier=}')

        quotient += multiplier

        remainder += buffer - denominator*multiplier
        retval += difficulty_of_difference(buffer, denominator*multiplier, radix, cache_size)

        buffer = remainder

    assert quotient == numerator // denominator, f'{quotient=}, {numerator=}, {denominator=}'

    return retval


def tuples_not_ending_in(tuples, end_digits_to_exclude):
    for tuple_ in tuples:
        if tuple_[0] % 10 in end_digits_to_exclude:
            continue
        yield tuple_


if __name__ == '__main__':


    levels = collections.defaultdict(list)


    # print(f'Factors: {list(prod_gen.two_products(N))}')
    
    for fraction in fractions(N):
        level = difficulty_of_long_division(*fraction)
        levels[level].append(fraction)




    for level in sorted(levels)[:-1]:
        fractions = levels[level]
        print(f'Level {level} fractions: {fractions}')



    hardest_level = max(levels)

    hardest_fractions = levels[hardest_level]


    print(f'Hardest Level (level {hardest_level}) fractions: {hardest_fractions}')

