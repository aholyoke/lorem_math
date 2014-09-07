from django.shortcuts import render_to_response, render
from django.http import HttpResponse, HttpResponseRedirect, Http404


def index(request):
	return render_to_response('index.html')
