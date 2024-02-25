import sys
import collections


N = int((sys.argv[1:2] or [100_000])[0])


def two_partitions(n = N):
    for i in range(1, (N // 2) + 1):
        yield i, N-i


def difficulty_of_sum(summands: tuple[int], radix: int = 10, cache_size = 3) -> int:
    
    cache = collections.deque([], maxlen=cache_size)

    x, y = summands

    if y < x:
        x, y = y, x
    
    assert x <= y

    carry = 0
    retval = 0

    result, multiplier = 0, 1

    while x > 0 or carry > 0:
        x, r_x = divmod(x, radix)
        y, r_y = divmod(y, radix)

        tuple_ = (r_x, r_y, carry)


        if tuple_ in cache:
            retval += 1
        elif r_x == r_y:
            # doubling can use fast look up in the 2-times table
            retval += min(r_x, 3) + carry
        elif r_x % 2 == 0 and r_y % 2 == 0:
            # subtract 1 if both digits are even
            retval += max(0, min(r_x, r_y)-1) + carry
        else:
            # add the smaller digit to the larger one, 
            # plus the carry bit.
            retval += min(r_x, r_y) + carry


        # Extra operation to add the carry.
        retval += carry

        cache.append(tuple_)

        carry, partial_sum = divmod(r_x + r_y + carry, radix)
        result += partial_sum*multiplier


        # Extra operation to store the carry
        retval += carry


        multiplier *= radix
        
    result += multiplier * y

    assert result == sum(summands), f'{result=}, {summands=}, {carry=}, {multiplier=}, {radix=}'

    return retval


levels = collections.defaultdict(list)


for summands in two_partitions():
    level = difficulty_of_sum(summands)
    levels[level].append(summands)


def sums_not_ending_in(sums, end_digits_to_exclude):
    for tuple_ in sums:
        if tuple_[0] % 10 in end_digits_to_exclude:
            continue
        yield tuple_



for level in sorted(levels)[:-1]:
    sums = levels[level]
    print(f'Level {level} sums: {sums[:4]},..,{sums[-4:]}')

    # exc_ending_in_5 = list(sums_not_ending_in(sums, [5]))
    # print(f'(exc ending in 5): {exc_ending_in_5[:4]},..,{exc_ending_in_5[-4:]}')


hardest_level = max(levels)

hardest_sums = levels[hardest_level]

print(f'Hardest sums (level: {hardest_level}): {hardest_sums[:4]},..,{hardest_sums[-4:]}')


# hardest_sums_not_ending_in_5 = list(sums_not_ending_in(hardest_sums, [5]))
# print(f'Hardest sums not ending in 5: {hardest_sums_not_ending_in_5[:4]},..,{hardest_sums_not_ending_in_5[-4:]}')
