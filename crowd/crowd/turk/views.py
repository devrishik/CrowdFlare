import datetime

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render


def welcome(request):
	key = request.GET.get('key', '')
	user_type = request.GET.get('user_type', '')

	now = datetime.datetime.now()

	html = "<html><body>It is now %s.</body></html>" % now
	# return HttpResponse(html + " " + user_type + " " + key)
	return render(request, 'turk/welcome.html', {
            'user_type': user_type
        })

