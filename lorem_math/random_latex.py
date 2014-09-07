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
    def __init__(self, num_equal_signs=0, random_seed=None):
        # Provide random_seed if you want to generate the same formula twice
        self.seed = seed
        seed(random_seed)

        self.formulae = []
        for i in range(num_equal_signs + 1):
            # We should convert this to nested lists if we want to do
            # any post-processing on the structure before flattening it.
            self.structure = self.start()
            self.formulae.append("".join(flatten_gen(self.structure)))

        self.formula = " = ".join(self.formulae)

    def one_of(self, *options):
        ''' self.one_of("x", "y") calls either self.random_x or self.random_y
        with equal likeliness '''
        return getattr(self, "random_" + choice(options))()

    def one_of_distribute(self, arg_dict={}, safe=True, **options_with_ratios):
        ''' self.one_of_distribute(x=(2,3), y=(1,3)) calls either self.random_x
        with 2/3 likeliness or self.random_y with 1/3 likeliness. When safe is
        True this function will check that the probabilities add to 1 '''
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
                return getattr(self, "random_" + option)(**arg_dict)

            # remaining - fraction
            remaining = (rem_num * frac_den - frac_num * rem_den,
                         frac_den * rem_den)

    def start(self):
        return self.random_expression()

    def random_expression(self, make_smaller=0, variables=None):
        ''' 0 <= make_smaller <= 100 '''
        variables = variables or []
        return self.one_of_distribute(
            arg_dict={'make_smaller': make_smaller, 'variables': variables},
            term=(300 + 2 * make_smaller, 1000),
            add_or_subtract=(550 - make_smaller, 1000),
            limit=(100 - make_smaller, 1000),
            function=(50, 1000))

    def random_function(self, make_smaller=0, variables=None):
        variables = variables or []
        yield choice(["f(", "g(", "h(", "sin(", "cos(", "tan(", "log(", "ln("])
        for i in range(randint(0, 2)):
            variable = self.random_variable(variables)
            variables.append(variable)
            yield variable
            yield ", "
        variable = self.random_variable(variables)
        variables.append(variable)
        yield variable
        yield ") = "
        yield self.random_expression(50, variables)

    def random_limit(self, make_smaller=0, variables=None):
        variables = variables or []
        yield "\lim_{"
        yield self.random_variable(variables)
        yield " \\to "
        yield self.one_of_distribute(
            number=(1, 3),
            infinity=(2, 3))
        yield "}"
        yield self.random_expression(max(25, make_smaller), variables)

    def random_infinity(self):
        return choice(["\infty", "-\infty"])

    def random_add_or_subtract(self, make_smaller=0, variables=None):
        variables = variables or []
        yield self.random_expression(50, variables)
        yield choice([" + ", " - "])
        yield self.random_term(10, variables)

    def random_term(self, make_smaller=0, variables=None):
        variables = variables or []
        return self.one_of_distribute(
            arg_dict={'make_smaller': make_smaller, 'variables': variables},
            multiply=(250, 1000),
            factor=(650 + make_smaller, 1000),
            fraction=(100 - make_smaller, 1000))

    def random_multiply(self, make_smaller=0, variables=None):
        variables = variables or []
        yield self.random_term(10, variables)
        yield self.random_factor(0, variables)

    def random_factor(self, make_smaller=0, variables=None):
        variables = variables or []
        yield self.one_of_distribute(
            arg_dict={'variables': variables},
            number=(5, 10),
            greek=(3, 10),
            variable=(2, 10))

        if chance(1, 5):
            yield self.random_sub_or_sup()

    def random_sub_or_sup(self):
        yield choice("_^")
        yield "{"
        yield self.random_expression(100)
        yield "}"

    def random_variable(self, variables=None):
        variables = variables or []
        if variables == []:  # generate a new variable
            return choice(["x", "y", "a", "b", "{\\theta}"])
        else:  # return a previously used variable
            return choice(variables)

    def random_greek(self, variables=None):
        return choice([
            "{\pi}",
            "{\sigma}",
            "{\Sigma}",
            "{\phi}",
            "{\lambda}",
            "{\psi}",
            "{\\theta}",
            "{\gamma}",
            "{\mu}",
            "{\Omega}",
            "{\\alpha}",
            "{\\beta}",
            "{\Gamma}",
            "{\epsilon}"])

    def random_fraction(self, make_smaller=0, variables=None):
        variables = variables or []
        yield "\\frac{"
        yield self.random_expression(max(80, make_smaller))
        yield "}{"
        yield self.random_expression(max(95, make_smaller))
        yield "}"

    def random_number(self, variables=None):
        yield choice("123456789")
        for i in range(randint(0, 3)):
            yield choice("01234567")
