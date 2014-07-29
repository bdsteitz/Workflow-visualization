from django.shortcuts import render, redirect
from django.contrib.auth.views import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext, ugettext_lazy as _
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm

@sensitive_post_parameters()
def login(request, template_name='login.html'):
	if request.user.is_authenticated():
		return redirect('display_main')
	elif not request.POST:
		next_url = request.REQUEST.get('next', '')
		context = {'next': next_url}
		return render(request, template_name, context)

	result = auth_login(request, template_name=template_name)
	if request.user.is_authenticated():
		messages.success(request, 'You successfully logged in!')

		next_url = request.REQUEST.get('next', '')
		try:
			return reverse(next_url)
		except:
			pass
	else:
		messages.error(request, 'Please try to login again. If this continues, contact us!')
	return result

def logout(request, template_name='logout.html'):
	auth_logout(request)
	return render(request, template_name=template_name)


def home(request):
	c = {}
	return render(request, 'index.html', c)
