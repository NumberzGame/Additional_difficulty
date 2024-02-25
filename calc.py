import sys
import collections


N = int((sys.argv[1:2] or [100_000])[0])


def two_partitions(n = N):
    for i in range(1, N):
        yield i, N-i


def human_difficulty_of_sum(summands: tuple[int], radix: int = 10, cache_size = 3) -> int:
    
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


        if tuple_ not in cache:
            retval += min(r_x, r_y) + carry
        else:
            retval += 1


        # Extra operation to add the carry.
        retval += carry

        cache.append(tuple_)

        carry, partial_sum = divmod(r_x + r_y + carry, radix)
        result += partial_sum*multiplier


        # Extra operation to store the carry
        retval += carry


        multiplier *= radix
        
    result += multiplier * y

    assert result == sum(summands), f'{result=}, {summands=}, {carry=}'

    return retval


print(f'Hardest sum: {max(two_partitions(), key= human_difficulty_of_sum)}')
