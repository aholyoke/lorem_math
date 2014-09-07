from django.shortcuts import render_to_response, render
from django.http import HttpResponse, HttpResponseRedirect, Http404

from random_latex import RandomFormula


def index(request):
    r = RandomFormula()
    context = {'formula': r.formula}
    return render_to_response('index.html', context)


def random_latex(request):
    num_equal_signs = int(request.GET.get('num_equal_signs', '0'))
    r = RandomFormula(num_equal_signs)
    context = {'formula': r.formula}
    return render_to_response('raw_page.html', context)
