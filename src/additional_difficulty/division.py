import sys
import collections
from typing import Iterator

from .products import digits
from .sum_of_two import difficulty_of_sum
from .differences import difficulty_of_difference


def fractions(n: int, max_: int) -> Iterator[tuple[int, int]]:
    for i in range(1, max_ - n + 1):
        yield n * i, i


def difficulty_of_long_division(
    numerator: int,
    denominator: int,
    radix: int = 10,
    cache_size: int = 3,
    ) -> float:

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

        # print(f'{buffer=}, {multiplier=}, {quotient=}')

        quotient += multiplier
        buffer -= denominator*multiplier
        remainder += buffer
        retval += difficulty_of_difference(buffer, denominator*multiplier, radix, cache_size)


    assert quotient == numerator // denominator, f'{numerator=}, {denominator=}, {quotient=}, {remainder=}'

    return retval


# TODO: Fix Bug:
# difficulty_of_long_division(300,2)


if __name__ == '__main__':


    N = int((sys.argv[1:2] or [123_456])[0])

    MAX = int((sys.argv[2:3] or [5000])[0])

    levels = collections.defaultdict(list)


    # print(f'Factors: {list(prod_gen.two_products(N))}')
    
    for fraction in fractions(N, MAX):
        level = difficulty_of_long_division(*fraction)
        levels[level].append(fraction)




    for level in sorted(levels)[:-1]:
        fractions = levels[level]
        print(f'Level {level} fractions: {fractions}')



    hardest_level = max(levels)

    hardest_fractions = levels[hardest_level]


    print(f'Hardest Level (level {hardest_level}) fractions: {hardest_fractions}')

