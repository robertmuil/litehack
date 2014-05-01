# Create your views here.
from django.http import HttpResponse
from django.utils import timezone
import hwaccess

batteries = [0, 1] #TODO: determine programmatically

def index(request):
	"""

	TODO: keep status updated asynchronously, so that this call never
	has to read external files etc. - this should always complete immediately.
	"""
	rgtnow = timezone.now()
	ac_plugged = hwaccess.is_plugged_in()

	respstr = "<h1>Welcome to <b>%s</b></h1>" % (hwaccess.get_hostname())
	respstr += "<p>Time now is %s</p>" % (str(rgtnow))
	respstr += "<p>AC is %s</p>" % ("Connected" if ac_plugged else "Disconnected")
	respstr += "<h2>Battery Status</h2>"
	respstr += "<ul>"
	for bat in batteries:
		#respstr += "<h3>%s</h3>"%(bat)
		respstr += "<li>%s</li>"%(hwaccess.get_batt_status(bat))
	respstr += "</ul>"

	return HttpResponse(respstr)
