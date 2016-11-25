import math
from math import sin, cos, tan
from math import sqrt, floor

import itertools
import copy


class Number:
    """ Class to represent a number stored in scientific notation
    Allows to have arbitrary precision operation
    """
    def __init__(self, val=None, exponent=0, sign=+1):
        self.val = [] if val is None else val  # List of decimals values (WARNING: No copy)
        self.exponent = exponent  # Decimal exponent
        self.sign = sign

    @staticmethod
    def from_str(str_n):
        """ Factory to build a number from a string
        WARNING: Do no handle exotic strings like '000.012', '1.234e-123',
        '00123' or 'hello123'
        Examples of supported string:
            123
            0.0057
            -43.7
        """
        val = []
        exponent = len(str_n)-1
        sign = +1

        if str_n.startswith('-'):
            sign = -1
            str_n = str_n[1:]
            exponent -= 1

        if '.' in str_n:
            exponent = str_n.find('.') - 1  # = 0 if str_n == 'x.xxxx'
            str_n = str_n.translate(None, '.')

            exponent -= len(str_n) - len(str_n.lstrip('0'))  # No effect if str_n == 'x.xxxx' or 'xxx.x'
            str_n = str_n.lstrip('0')
        val = [int(char) for char in reversed(str_n)]  # Could also use ord(char)-ord('0')

        return Number(val, exponent, sign)

    def __str__(self):
        """ String representation of the number
        """
        chars = [chr(ord('0') + i) for i in reversed(self.val)]
        decimal = len(chars)-1
        if self.exponent < 0:  # Of the form 0.01234
            chars = ['0.'] + ['0']*(-1-self.exponent) + chars
        elif self.exponent < decimal:  # Of the form 12.34
            chars.insert(self.exponent+1, '.')
        elif self.exponent > decimal:  # Of the form 123400
            chars = chars + ['0']*(self.exponent - decimal)
        if self.sign < 0:
            chars = ['-'] + chars
        return ''.join(chars)

    def _add_base(a, b):
        """ Simple addition. Don't check the signs here
        """
        result = Number()
        result.exponent = max(a.exponent, b.exponent)

        # Add compute padding for the smallest exponent
        low_self = a.exponent - len(a.val) + 1
        low_b = b.exponent - len(b.val) + 1
        lowest, highest = (a, b) if low_self < low_b else (b, a)

        carry = 0
        for val_a, val_b in itertools.izip_longest(
            lowest.val,
            [0]*abs(low_self-low_b) + highest.val,  # Right padding
            fillvalue=0  # Left padding
        ):
            addition = val_a + val_b + carry
            result.val.append(addition % 10)
            carry = addition // 10

        if carry > 0:
            result.val.append(carry)
            result.exponent += 1

        return result

    def __add__(self, other):
        """ Arithmetic addition
        """
        if self.sign == other.sign:  # Simple case
            result = Number._add_base(self, other)
            result.sign = self.sign
        else:  # Signs don't match
            # Compute abs(max)-abs(min) and set the sign to the max
            abs_self = self.to_abs()
            abs_other = other.to_abs()
            min_n, max_n, sign = (abs_self, abs_other, other.sign) if abs_self < abs_other else (abs_other, abs_self, self.sign)
            result = Number(
                [-val for val in min_n.val],
                min_n.exponent
            )
            result = Number._add_base(max_n, result)
            result.sign = sign

        return result.lstrip()

    def __sub__(self, other):
        """ Arithmetic substraction
        """
        other.sign *= -1
        result = self + other  # a - b == a + (-b)
        other.sign *= -1  # Restore the sign
        return result

    def _mul_base(self, n):
        """ Multiply by base number 0/9 and return a new number
        Return positive number (sign managed later)
        """
        assert(0 <= n <= 9)
        if n == 0:
            return Number([0])

        result = Number()
        result.exponent = self.exponent

        carry = 0
        for val in self.val:
            multiplication = val*n + carry
            result.val.append(multiplication % 10)
            carry = multiplication // 10

        if carry > 0:
            result.val.append(carry)
            result.exponent += 1

        return result

    def _mul_10(self, n):
        """ Shift the values on the left or right
        Return positive number (sign managed later)
        Warning: only used in __mul__ so no need to duplicate the values
        """
        return Number(self.val, self.exponent + n)  # Warning: The values are not copied but passed by reference

    def __mul__(self, other):
        """ Arithmetic multiplication
        Could be optimised, specially when we don't need full precision
        """
        short_n, long_n = (self, other) if len(self.val) < len(other.val) else (other, self)

        values_cached = {}  # Avoid recomputing _mul_base each time

        result = Number([0])
        for i, val in enumerate(short_n.val):
            result += values_cached.setdefault(val, long_n._mul_base(val))._mul_10(short_n.exponent-len(short_n.val) + i + 1)
        result.sign = self.sign * other.sign

        return result

    def to_floor(self):
        """ Keep only the integer part of the number
        Warning: negative exponent and negative numbers not supported
        """
        return Number(copy.copy(self.val[max(0, len(self.val) - self.exponent - 1):]), self.exponent)

    def to_ceil(self):
        """ Keep only the integer part rounded up
        Warning: negative exponent and negative numbers not supported
        """
        if sum(self.val[:min(len(self.val), len(self.val) - self.exponent - 1)]) == 0:
            return self.to_floor()
        return (self.to_floor() + Number.from_str('1')).to_floor()

    def to_abs(self):
        """ Positive value
        """
        return Number(copy.copy(self.val), self.exponent, +1)

    def to_round(self):
        """ Return the closest integer
        """
        if (self.exponent >= 0 and  # Filter 0.00... (WARNING: 0.9 won't work)
            len(self.val) - 1 >= self.exponent + 1 and  # Filter 12300...
            self.val[len(self.val) - 1 - (self.exponent + 1)] > 5):
            return self.to_ceil()
        else:
            return self.to_floor()

    def truncate(self, nb_keep):
        """ Simplify the number of decimal when we don't need precision anymore
        Modify the current number (no copy)
        """
        self.val = self.val[max(0, len(self.val) - nb_keep):]
        return self

    def __lt__(self, other):
        """ Compare the two given number
        Warning: Only strictly positive number supported (0 Not supported !!)
        """
        if self.exponent != other.exponent:
            return self.exponent < other.exponent
        for a, b in itertools.izip_longest(reversed(self.val), reversed(other.val), fillvalue=0):
            if a < b:
                return True
            elif b < a:
                return False
        return False  # Equality

    def lstrip(self):
        """ Remove the left zeros and shift the exponent
        Warning: 0 Not supported
        """
        result = Number(list(reversed(list(
            itertools.dropwhile(lambda x: x == 0, reversed(self.val))
            ))), self.exponent, self.sign)
        if len(result.val) == 0:
            result.val = [0]
            result.sign = +1
        result.exponent -= len(self.val) - len(result.val)
        return result

    def is_even(self):
        """ Return True is the number is even
        Check on the truncated version of the number (Numbers like 1.23e5
        and negative exponent not supported)
        """
        if not len(self.val) or self.to_floor().val[0] % 2:
            return True
        return False


def answer(str_n):
    sqrt_2 = Number.from_str('1.41421356237309504880168872420969807856967187537694807317667973799073247846210703885038753432764157273501384623091229702492483605585073721264412149709993583141322266592750559275579995050115278206057147010955997160597027453459')
    div_2 = Number.from_str('0.5')
    one = Number.from_str('1')

    n = Number.from_str(str_n)

    # Approximation which will give the right result +/-1
    candidate_str = (sqrt_2 * n * (n + one) - n) * div_2
    return str(candidate_str.to_round())


# Save some computation time
CACHE_TAYLOR_COEF = [
    (Number.from_str('1'), Number.from_str('-0.266255342041'),Number.from_str('-0.5187')),
    (Number.from_str('2'), Number.from_str('-0.858216185669'),Number.from_str('0.4871')),
    (Number.from_str('6625109'), Number.from_str('-1'),Number.from_str('-0.4566')),
    (Number.from_str('5'), Number.from_str('-0.975179482214'),Number.from_str('-0.4516')),
    (Number.from_str('12'), Number.from_str('-0.99572678525'),Number.from_str('0.4512')),
    (Number.from_str('2744210'), Number.from_str('-1'),Number.from_str('0.4511')),
    (Number.from_str('1136689'), Number.from_str('-1'),Number.from_str('-0.4503')),
    (Number.from_str('29'), Number.from_str('-1'),Number.from_str('-0.4502')),
    (Number.from_str('70'), Number.from_str('-1'),Number.from_str('0.4502')),
    (Number.from_str('470832'), Number.from_str('-1'),Number.from_str('0.4502')),
    (Number.from_str('169'), Number.from_str('-1'),Number.from_str('-0.4502')),
    (Number.from_str('408'), Number.from_str('-1'),Number.from_str('0.4502')),
    (Number.from_str('80782'), Number.from_str('-1'),Number.from_str('0.4502')),
    (Number.from_str('985'), Number.from_str('-1'),Number.from_str('-0.4502')),
    (Number.from_str('13860'), Number.from_str('-1'),Number.from_str('0.4502')),
    (Number.from_str('2378'), Number.from_str('-1'),Number.from_str('0.4502')),
    (Number.from_str('5741'), Number.from_str('-1'),Number.from_str('-0.4502')),
    (Number.from_str('195025'), Number.from_str('-1'),Number.from_str('-0.4502')),
    (Number.from_str('33461'), Number.from_str('-1'),Number.from_str('-0.4502')),
    (Number.from_str('3'), Number.from_str('0.723264630163'),Number.from_str('0.2413')),
    (Number.from_str('7'), Number.from_str('0.950565000973'),Number.from_str('-0.2300')),
    (Number.from_str('9369319'), Number.from_str('1'),Number.from_str('-0.2272')),
    (Number.from_str('17'), Number.from_str('0.991459660759'),Number.from_str('0.2255')),
    (Number.from_str('41'), Number.from_str('0.998532977831'),Number.from_str('-0.2252')),
    (Number.from_str('1607521'), Number.from_str('1'),Number.from_str('-0.2251')),
    (Number.from_str('99'), Number.from_str('1'),Number.from_str('0.2251')),
    (Number.from_str('239'), Number.from_str('1'),Number.from_str('-0.2251')),
    (Number.from_str('275807'), Number.from_str('1'),Number.from_str('-0.2251')),
    (Number.from_str('577'), Number.from_str('1'),Number.from_str('0.2251')),
    (Number.from_str('1393'), Number.from_str('1'),Number.from_str('-0.2251')),
    (Number.from_str('3363'), Number.from_str('1'),Number.from_str('0.2251')),
    (Number.from_str('8119'), Number.from_str('1'),Number.from_str('-0.2251')),
    (Number.from_str('19601'), Number.from_str('1'),Number.from_str('0.2251')),
    (Number.from_str('47321'), Number.from_str('1'),Number.from_str('-0.2251')),
    (Number.from_str('114243'), Number.from_str('1'),Number.from_str('0.2251')),
    (Number.from_str('665857'), Number.from_str('1'),Number.from_str('0.2251')),
    (Number.from_str('3880899'), Number.from_str('1'),Number.from_str('0.2249')),
]

def taylor_term(n):
    """ Approximate the infinite sum
    """
    INV_2PI = Number.from_str('0.15915494309189533576888376337251436203445964574045644874766734405889679763422653509011380276625308595607284272675795803689291184611457865287796741073169983922923996693740907757307')
    INV_4 = Number.from_str('0.25')
    INV_2 = Number.from_str('0.5')
    NB_16 = Number.from_str('16')
    NB_1 = Number.from_str('1')
    NB_2 = Number.from_str('2')
    NB_COS_P = Number.from_str('0.225')
    NB_2PISQRT = Number.from_str('8.885765876316732494031761980121387397229243378751380446170')
    NB_SQRT2 = Number.from_str('1.4142135623730950488016887242096980785696718753769480731766797379907324784621070388503875343276415727350')

    n_shifted = (n + INV_2) * NB_SQRT2

    def get_term2(k, n):
        """ Fast approximation of the Cosinus
        Input in radiant
        """
        x = n_shifted * k
        x = x - (INV_4 + (x + INV_4).to_floor())
        x.truncate(6)  # No need to have full precision after that
        x = x * NB_16 * (x.to_abs() - INV_2)
        x = x + NB_COS_P * x * (x.to_abs() - NB_1)
        return x.truncate(4)

    def get_factor(coeff):
        k_str = coeff[0]
        factor = (coeff[1] - get_term2(k_str, n)) * coeff[2]
        return factor

    # Compute Sum_0^Inf (cos(x/2)-cos((n+0.5)x))/sin(x/2)
    return NB_2*INV_2PI * sum([get_factor(coeff) for coeff in CACHE_TAYLOR_COEF[1:]], get_factor(CACHE_TAYLOR_COEF[0]))


def answer2(n):
    """ Second approximation, using the fact that
    floor(x*sqrt(2)) + floor(n-x*sqrt(2)) = Pulse wave
    """
    # Ending value
    top_value = (sqrt_2*n).to_floor()
    bottom_value = top_value - one

    # Top/bottom count:
    tau_T = (sqrt_2*n) - (sqrt_2*n).to_floor()
    nb_terms = ((n + one)*div_2).to_ceil()
    count_top = (nb_terms * tau_T).to_ceil()  # Approximate value (+/- 1)
    count_bottom = nb_terms - count_top

    # Deduce the result
    candidate_str = count_top*top_value + count_bottom*bottom_value
    if not n.is_even():
        middle_value = (n * div_2 * sqrt_2).to_floor()
        candidate_str = candidate_str - middle_value

    return str(candidate_str.to_round())


def ground_truth(ni):
    y1_float = [i*sqrt(2) for i in range(ni+1)] # frac(sum(exacts)) = fract(sum(fract(diff)))
    y1_floor = [floor(exact) for exact in y1_float]
    return sum(y1_floor)
