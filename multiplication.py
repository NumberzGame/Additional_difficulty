import sys
import math
import collections
from typing import Iterator, Iterable

start_x = int((sys.argv[1:2] or [100_000])[0])

class ErathosthenesFactoriser:

    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]

    # not primes, sieved out
    # composites = set()
    # Stand in for an OrderedSet 
    composites = {}

    all_primes_known_up_to_inclusive = 31

    def __init__(self, primes: list[int] = None):

        if primes is not None:
            self.primes = primes

        assert any(x % 2 for x in self.primes), "ErathosthenesFactoriser.primes must contain 3"
        assert self.primes[0] == 2 and self.primes[1] == 3, """primes must contain 2 and 3, and 
                                                               be in ascending order, (and 1 is 
                                                               not a prime by convention)""".replace('  ','')

    def factorise(self, x: int) -> dict[int, int]:
        """  Side effects:
              - updates cached primes
              - saves factorisation in prime_factorisation
        """

        start_x = x

        prime_factorisation = collections.Counter()

        # Factor out 2s now, so we when testing prime candidates
        # the highest known prime is always odd, and we can 
        # always skip forward 2 at a time from it.
        while x % 2 == 0:
            prime_factorisation.update([2])
            x //= 2

        assert x % 2,  f"All 2s should've been factored from {x=}: {self.start_x=}, {prime_factorisation=}"

        test_up_to_inclusive = math.isqrt(x)

        # 2s already factored out.  Start from primes[1] == 3
        i = 1

        while True:

            r = 0
            p = self.primes[i]



            q, r = divmod(x, p)

            if r == 0:
                prime_factorisation.update([p])
                x = q
                test_up_to_inclusive = math.isqrt(x)
                continue  # Repeat without incrementing i
                          # until there are no more factors
                          # of p in x
                

            if p > test_up_to_inclusive:
                # All prime factors have been divided out up to 
                # some prime p**2 > x.  Therefore x is prime. 
                prime_factorisation.update([x])
                if x not in self.primes:
                    self.primes.append(x)
                break

            i += 1

            if self.all_primes_known_up_to_inclusive > test_up_to_inclusive:
                continue  # We already know all the primes needed
                          # to factor x

            self.sieve_multiples_of(p, test_up_to_inclusive)




        check = 1

        for prime, exponent in prime_factorisation.items():
            check *= prime**exponent

        assert check == start_x

        return prime_factorisation


    def sieve_multiples_of(self, p: int, test_up_to_inclusive: int):
        # Sieve out multiples of p, an odd prime.  
        # p**2 is the lowest composite number that cannot
        # already have been sieved out as a factor of 
        # 2, 3, ..., p-1
        # Requires self.primes to contain at least 2 and 3 
        # so that self.primes[-1] is odd.

        sieve_up_to_inclusive = max(test_up_to_inclusive, 
                                    next(p**2 
                                         for p in self.primes
                                         if p**2 >= test_up_to_inclusive
                                        )
                                   )

        print(f'Sieving {p} up to {sieve_up_to_inclusive}')

        for composite in range(p**2, sieve_up_to_inclusive + 1, 2*p):
            print(f'Adding {composite=}')
            # self.composites.add(composite)
            self.composites[composite] = None

        start = self.primes[-1] + 2
        if start < p**2:
            print(f'searching for new primes from: {start}')
            for candidate in range(start, p**2, 2):
                if candidate not in self.composites:
                    print(f'''New prime: {candidate} found! 
                            ({p=}, bound: {test_up_to_inclusive} )'''.replace('  ','')
                        )
                    self.primes.append(candidate)

        if p**2 > self.all_primes_known_up_to_inclusive:
            print(f'Updating to primes known bounds to {p**2}')
            self.all_primes_known_up_to_inclusive = p**2

if __name__ == '__main__':
    ef = ErathosthenesFactoriser()
    # for prime in ef.primes_from_factoring(start_x):

    prime_factorisation = ef.factorise(start_x)

    print(f'\nPrime factorisation of {start_x}: ' + 
          '*'.join(f'({prime}**{power})' if power >= 2 else f'{prime}'
                   for prime, power in prime_factorisation.items()
                  )
         )

    print(f'Primes: {ef.primes}')
    print(f'Composites: {list(ef.composites)}')