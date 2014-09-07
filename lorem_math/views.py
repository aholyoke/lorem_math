from django.shortcuts import render_to_response, render
from django.http import HttpResponse, HttpResponseRedirect, Http404

from random_latex import RandomFormula


def index(request):
    num_equal_signs = int(request.GET.get('num_equal_signs', '0'))
    seed = request.GET.get('seed', '')
    if seed == '':
        r = RandomFormula(num_equal_signs)
    else:
        r = RandomFormula(num_equal_signs, int(seed))
    context = {'formula': r.formula}
    return render_to_response('index.html', context)


def random_latex(request):
    num_equal_signs = int(request.GET.get('num_equal_signs', '0'))
    r = RandomFormula(num_equal_signs, None)
    context = {'formula': r.formula}
    return render_to_response('raw_page.html', context)


def just_render(request, formula):
    return render_to_response('just_render.html', {'formula': formula})
