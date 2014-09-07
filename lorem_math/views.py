from django.shortcuts import render_to_response, render
from django.http import HttpResponse, HttpResponseRedirect, Http404

from random_latex import *

def index(request):
	r = RandomFormula()
	context = {'formula': r.formula}
	return render_to_response('index.html', context)


''' For when we want to load the LaTeX asynchronously or on a different page etc '''
# def random_latex(request):
# 	r = RandomFormula()
# 	context['formula'] = r.formula
# 	return render_to_response('index.html', context)