# Create your views here.
from django.http import HttpResponse
from django.utils import timezone

def index(request):
	rgtnow=timezone.now()
	respstr = "<b>Wello</b>, Horld. <p>Poor prior pristine papers!</p>"
	respstr += "<ul><li>Time now is %s</li></ul>" % (str(rgtnow))

	return HttpResponse(respstr)
