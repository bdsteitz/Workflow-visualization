from django.shortcuts import render, redirect

def home(request):
	c = {}
	return render(request, 'index.html', c)

def test(request):
	c = {'my_var': 'bang'}
	return render(request, 'index.html', c)



