from django.shortcuts import render

# Create your views here.

def test(request):
	print 'hi'
	c = {}
	return render(request, 'blah.html', c)
