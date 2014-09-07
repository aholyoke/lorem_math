from random import choice, randint, seed
from copy import deepcopy, copy
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
        self.formula = "\\\\ = ".join(self.formulae)

    def one_of(self, *options):
        ''' self.one_of("x", "y") calls either self.random_x or self.random_y
        with equal likeliness '''
        return getattr(self, "random_" + choice(options))()

    def one_of_distribute(self, context, safe=True, **options_with_ratios):
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
                return getattr(self, "random_" + option)(context)

            # remaining - fraction
            remaining = (rem_num * frac_den - frac_num * rem_den,
                         frac_den * rem_den)

    def start(self):
        context = {'make_smaller': 0, 'variables': []}
        return self.random_expression(context)

    def random_expression(self, context):
        make_smaller = context['make_smaller']
        return self.one_of_distribute(
            context,
            term=(300 + 2 * make_smaller, 1000),
            add_or_subtract=(550 - make_smaller, 1000),
            limit=(100 - make_smaller, 1000),
            function=(50, 1000))

    def random_function(self, context):
        # We need a deepcopy context here since variables may be added
        new_context = deepcopy(context)
        yield choice(["f(", "g(", "h(", "sin(", "cos(", "tan(", "log(", "ln("])
        for i in range(randint(0, 2)):
            variable = self.random_variable(new_context)
            new_context['variables'].append(variable)
            yield variable
            yield ", "
        variable = self.random_variable(new_context)
        new_context['variables'].append(variable)
        yield variable
        yield ") = "
        yield self.random_expression(new_context)

    def random_limit(self, context):
        new_context = deepcopy(context)
        yield "\lim_{"
        variable = self.random_variable(new_context)
        new_context['variables'].append(variable)
        yield variable
        yield " \\to "
        yield self.one_of_distribute(
            new_context,
            number=(1, 3),
            infinity=(2, 3))
        yield "}"
        new_context['make_smaller'] = max(25, new_context['make_smaller'])
        yield self.random_expression(new_context)

    def random_infinity(self, context):
        return choice(["\infty", "-\infty"])

    def random_add_or_subtract(self, context):
        new_context = copy(context)
        new_context['make_smaller'] = 50
        yield self.random_expression(new_context)
        yield choice([" + ", " - "])
        new_context = copy(context)
        new_context['make_smaller'] = 10
        yield self.random_term(new_context)

    def random_term(self, context):
        make_smaller = context['make_smaller']
        return self.one_of_distribute(
            context,
            multiply=(2900, 10000),
            factor=(7000 + make_smaller, 10000),
            fraction=(100 - make_smaller, 10000))

    def random_multiply(self, context):
        new_context = copy(context)
        new_context['make_smaller'] = 10
        yield self.random_term(new_context)
        yield self.random_factor(new_context)

    def random_factor(self, context):
        yield self.one_of_distribute(
            context,
            number=(5, 10),
            greek=(3, 10),
            variable=(2, 10))

        if chance(100 - context['make_smaller'], 500):
            yield self.random_sub_or_sup(context)

    def random_sub_or_sup(self, context):
        yield choice("_^")
        yield "{"
        yield self.random_expression(context)
        yield "}"

    def random_variable(self, context):
        variables = context['variables']
        if variables == [] or chance(1, 3):  # generate a new variable
            return choice(["x", "y", "a", "b", "{\\theta}"])
        else:  # return a previously used variable
            return choice(variables)

    def random_greek(self, context):
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

    def random_fraction(self, context):
        yield "\\frac{"
        new_context = copy(context)
        new_context['make_smaller'] = 100
        yield self.random_expression(new_context)
        yield "}{"
        yield self.random_expression(new_context)
        yield "}"

    def random_number(self, context):
        yield choice("123456789")
        for i in range(randint(0, 3)):
            yield choice("01234567")
