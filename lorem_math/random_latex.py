from random import choice, randint, seed
'''
Example Usage:

>>> r = RandomFormula()
>>> r.formula
'\\frac{\\psi + b66 + 302}{y - \\frac{645}{a - 875 - \\frac{\\lambda58}{x + 347261} - 7176}3870547}'
>>> r = RandomFormula(33)
>>> r.formula
'6474 + a - \\pi'
>>> r = RandomFormula(33)
>>> r.formula
'6474 + a - \\pi'
'''


def chance(numerator, denominator):
    ''' chance(3, 5) returns True 3/5 of the time
    numerator and denominator are integral
    denominator is non zero
    '''
    try:
        return randint(1, denominator) <= numerator
    except ValueError:
        if isinstance(denominator, int) and isinstance(denominator, int):
            raise ValueError("chance requires the denominator to be non-zero")
        else:
            raise ValueError("chance requires integral arguments")


def flatten_gen(gen):
    ''' Takes arbitrarily nested levels of generators and flattens them into
    one generator'''
    import types
    for i in gen:
        if isinstance(i, types.GeneratorType):
            for j in flatten_gen(i):
                yield j
        else:
            yield i


class RandomFormula(object):
    def __init__(self, random_seed=None):
        # Provide random_seed if you want to generate the same formula twice
        self.seed = seed
        seed(random_seed)
        self.formula = "".join(flatten_gen(self.start()))

    def one_of(self, *options):
        ''' self.one_of("x", "y") calls either self.random_x or self.random_y
        with equal likeliness '''
        return getattr(self, "random_" + choice(options))()

    def one_of_distribute(self, safe=True, **options_with_ratios):
        ''' self.one_of_distribute(x=(2,3), y=(1,3)) calls either self.random_x
        with 2/3 likeliness or self.random_y with 1/3 likeliness. When safe is
        True this function will check that the probabilities add to 1
        '''
        if safe:
            # eg. {x:(2,3), y:(1,3)} gives 1 * 3 * 3 = 9
            product_of_denominators = reduce(
                lambda agg, fraction: agg * fraction[1],
                options_with_ratios.values(), 1
            )
            # eg. {x:(2,3), y:(1,3)} gives 2 * (9 // 3) + 1 * (9 // 3)
            #                            = 2 * 3 + 1 * 3 = 9
            sum_of_numerators = sum(
                numerator * (product_of_denominators // denominator)
                for numerator, denominator in options_with_ratios.values()
            )
            assert product_of_denominators == sum_of_numerators

        remaining = (1, 1)

        for option, fraction in options_with_ratios.items():
            frac_num, frac_den = fraction[0], fraction[1]
            rem_num, rem_den = remaining[0], remaining[1]
            if chance(frac_num * rem_den, frac_den * rem_num):
                return getattr(self, "random_" + option)()

            # remaining - fraction
            remaining = (rem_num * frac_den - frac_num * rem_den,
                         frac_den * rem_den)

    def start(self):
        return self.random_expression()

    def random_expression(self):
        return self.one_of_distribute(term=(1, 2), add_or_subtract=(1, 2))

    def random_add_or_subtract(self):
        yield self.random_term()
        yield choice([" + ", " - "])
        yield self.random_expression()

    def random_term(self):
        return self.one_of_distribute(
            multiply=(2, 9),
            factor=(2, 3),
            fraction=(1, 9))

    def random_multiply(self):
        yield self.random_term()
        yield self.random_factor()

    def random_factor(self):
        return self.one_of_distribute(
            number=(2, 3),
            greek=(1, 9),
            variable=(2, 9))

    def random_variable(self):
        return choice("xyab")

    def random_greek(self):
        return choice(["\pi", "\sigma", "\phi", "\lambda", "\psi"])

    def random_fraction(self):
        yield "\\frac{"
        yield self.random_expression()
        yield "}{"
        yield self.random_expression()
        yield "}"

    def random_number(self):
        yield choice("123456789")
        for i in range(randint(0, 5)):
            yield choice("01234567")
