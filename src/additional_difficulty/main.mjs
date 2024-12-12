

const difficultyOfSumOfDigits = function(d_x, d_y) {
    // 0 <= d_x, d_y (both integers) <= 9
    
    if (d_x === d_y) {
        // # doubling can use fast look up in the 2-times table
        return Math.min(d_x, 3);
    }

    if ((d_x % 2 === 0) && (d_y % 2 === 0)) {
        // # subtract 1 if both digits are even
        return Math.max(1, Math.min(d_x, d_y)-1);
    }
    // # add the smaller digit to the larger one, 
    // # plus the carry bit.
    return Math.min(d_x, d_y, 1);
}



export const difficultyOfSum = function(summands, radix = 10, cache_size = 3) {
    
    let cache = []; // collections.deque([], maxlen=cache_size)

    let [x, y] = summands;

    if (y < x) {
        x, y = y, x;
    }

    // assert x <= y

    let carry = 0;
    let retval = 0.0;

    let [result, multiplier] = [0, 1];



    while ((x > 0) || (carry > 0)) {
        const r_x = x % radix;
        const r_y = y % radix;
        x = (x - r_x) / radix;
        y = (y - r_y) / radix;

        const tuple_ = (r_x, r_y, carry);


        if (cache.includes(tuple_)) {
            retval += 1;
        } else {
            retval += difficultyOfSumOfDigits(r_x, r_y);
            // # Extra operation to compute the carry.
            retval += carry;
        }

        // # Extra operation to add the carry.
        retval += carry;

        // Mimic a deque.  cache should only hold up 
        // to the last cache_size tuple_s
        cache = [...cache.slice(-(cache_size-1)), tuple_];

        const partialSum = (r_x + r_y + carry) % radix;
        carry = (r_x + r_y + carry - partialSum) / radix;
        result += partialSum*multiplier


        // # Extra operation to store the carry
        retval += carry;


        multiplier *= radix;
    }
        
    result += multiplier * y;

    if (result !== sum(summands)) {
        throw new Error(`Result: ${result} != sum of: ${summands}. `+
                        `Carry: ${carry}, Multiplier: ${multiplier}, Radix: ${radix}`
        );
    }

    return Math.max(1, retval);
}


// function(minuend: int, subtrahend: int, radix: int = 10, cache_size: int = 3) -> float:
export const difficultyOfDifference = function(minuend, subtrahend, radix = 10, cache_size = 3){
       
    let cache = [];

    if (minuend < subtrahend) {
        [minuend, subtrahend] = [subtrahend, minuend];
    }

    let [m, s] = [minuend, subtrahend];

    
    // assert m >= s

    let borrow = 0;
    let retval = 0;

    let [result, multiplier] = [0, 1];

    while ((s > 0) || (borrow > 0)) {
        let r_m = m % radix;
        const r_s = s % radix;
        m = (m - r_m) / radix;
        s = (s - r_s) / radix;
        // m, r_m = divmod(m, radix)
        // s, r_s = divmod(s, radix)

        const tuple_ = [r_m, r_s, borrow];

        r_m -= borrow;

        if (r_s > r_m) {
            borrow = 1;
        } else {
            borrow = 0;
        }

        if (r_m === r_s) {
            // # Zero difference
            // pass
        } else if (r_s + 1 === radix) {
            // # subtract 9 <=> add 10 & subtract 1
            retval += 1;
        } else if (cache.includes(tuple_)) {
            // # Recall result of the same operation, recently done. 
            retval += 1;
        } else if (2*r_s === r_m) {
            // # Subtract half of self is not so hard.
            retval += Math.min(r_s, 2);
        } else if ((r_m % 2 === 0) && (r_s % 2 === 0)) {
            // # subtract 1 if both digits are even
            retval += Math.max(1, r_s - 1);
        } else {
            // # the borrowed-bit allows larger digits to be subtracted,
            // # don't add extra difficulty for the borrow.
            retval += r_s;
            // # min(r_m - r_s, r_s)
        }

        // # Extra operation to add the borrow.
        retval += borrow;

        cache = [...cache.slice(-(cache_size-1)), tuple_];

        const partial_sum_of_diff = radix*borrow + r_m - r_s;
        result += partial_sum_of_diff*multiplier;


        // # Extra operation to store the borrowed bit
        retval += borrow;


        multiplier *= radix;
    }
        
    result += multiplier * m;

    if (result !== minuend - subtrahend) {
        throw new Error(`$Result: {result}, !== ${minuend} - ${subtrahend}. `+
                        `m: ${m}, s: ${s}, borrow: ${borrow}, `+
                        `multiplier: ${multiplier}, radix: ${radix}`);
    }

    return Math.max(1, retval);
}


// (x: int, radix: int = 10) -> Iterator[int]:
const digits = function(x, radix = 10) {
    return Array.from(x.toString(radix)).map((x) => parseInt(x, radix));
}


// def difficultyOfProductOfDigits(d_1: int, d_2: int, radix: int = 10) -> int:
export const difficultyOfProductOfDigits = function(d_1, d_2, radix = 10) {
    
    const product = d_1 * d_2;
    
    if ((product === 0) || [d_1, d_2].includes(1)){
        return 1;
    }

    if (product <= radix) {
        // # 2*3, ..., 2*5 and 3*3
        return 2;
    }

    if (radix % d_1 === 0 || radix % d_2 === 0 || product <= 2.4 * radix) {
        // # 2, 5 or a power of 2
        return 3;
    }

    if (product === 49) {
        // 7 x 7 is hardest!
        return 5;
    }

    // Every other product of digits to 81 
    // arbitrarily deemed to merit difficulty 4.
    return 4;
}
    


// (factors: tuple[int, int], radix: int = 10, cache_size = 3) -> float:
export const difficultyOfProduct = function(factors, radix = 10, cache_size = 3) {
    
    let cache = []; //: collections.deque[tuple[int, int, int]] = collections.deque([], maxlen=cache_size)

    let [a, b] = factors;

    if (a > b) {
        [a, b] = [b, a];
    }
    
    // assert a <= b

    if (a === 1) {
        return 1;
    }

    let retval = 0.0;

    let [result, multiplier] = [0, 1];

    // # Grid multiplication.

    const digits_a = digits(a);
    const digits_b = digits(b);
`
    // for (i, d_a), (j, d_b) in itertools.product(
    //                                     enumerate(digits(a)),
    //                                     enumerate(digits(b)),
    //                                     ):`

    for (const [i, d_a] of digits_a.entries()) {
        for (const [j, d_b] of digits_b.entries()) {


            const tuple_ = [d_a, d_b];

            if (cache.includes(tuple_)) {
                retval += 1;
            } else {
                retval += difficultyOfProductOfDigits(d_a, d_b);
                // # TODO: cache.append(tuple_)
                // cache = [...cache.slice(-(cache_size-1)), tuple_];
            }

            const partial_sum = d_a * d_b * (radix ** (i + j));


            retval += difficultyOfSum([result, partial_sum], radix, cache_size);

            result += partial_sum;

        }
    }

    // assert result == math.prod(factors), f'{result=}, {math.prod(factors)=}'
    if (result !== a * b) {
        throw new Error(`result: ${result} != a*b, a: ${a}, b: ${b}`);
    }


    return Math.max(1, retval);
}



// def difficulty_of_long_division(
//     numerator: int,
//     denominator: int,
//     radix: int = 10,
//     cache_size: int = 3,
//     ) -> float:
export const difficultyOfLongDivision = function(numerator, denominator, radix = 10, cache_size = 3) {
    // assert numerator % denominator == 0, f'{numerator=}, {denominator=}.  Division with remainder not implemented yet'


    const numerator_digits = digits(numerator, radix).reverse();

    let buffer = 0;
    let remainder = 0;

    let retval = 0.0;

    let quotient = 0;

    for (const digit of numerator_digits) {

        buffer *= radix;
        quotient *= radix;
        remainder *= radix;

        buffer += digit;

        if (buffer < denominator) {
            // # compare sizes
            retval += 1;
            continue;
        }

        let multiplier = 0;

        while (denominator * (multiplier + 1) <= buffer) {
            retval += difficultyOfSum((denominator * multiplier, denominator), radix, cache_size);

            // # Surely this should be retval += 1 ?  
            // # TODO:  Correct and rebuild cache.
            // # compare sizes
            // # compare sizes
            retval + 1; //# pyright: ignore[reportUnusedExpression];
            
            multiplier += 1;
        }

        // # print(f'{buffer=}, {multiplier=}, {quotient=}')

        quotient += multiplier;
        buffer -= denominator*multiplier;
        remainder += buffer;
        retval += difficultyOfDifference(buffer, denominator*multiplier, radix, cache_size);
    }

    // assert quotient == numerator // denominator, f'{numerator=}, {denominator=}, {quotient=}, {remainder=}'

    return Math.max(1, retval);
}

// # TODO: Fix Bug:
// # difficulty_of_long_division(300,2)