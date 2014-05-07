# Create your views here.
from django.http import HttpResponse
from django.utils import timezone
import hwaccess

use_direct_access=False #Allows bypassing database and hitting hw directly.

if not use_direct_access:
	from battstat.models import Batt

unknownstr = "<em>unknown</em>"

def index(request):
	"""

	"""
	on_ac = False

	hostname = hwaccess.get_hostname()
	nowstr = str(timezone.now())
	if use_direct_access:
		on_ac = hwaccess.on_ac()
		batteries = hwaccess.batteries()
	else:
		on_ac = hwaccess.on_ac() #TODO: store and pull ac adapter status from database
		batteries = Batt.objects.all()

	respstr = "<h1>Welcome to <b>%s</b></h1>" % (hostname)
	respstr += "<p>Time now is %s</p>" % (nowstr)
	respstr += "<p>AC is %s</p>" % ("Connected" if on_ac else "Disconnected")
	respstr += "<h2>Battery Status</h2>"
	respstr += "<ul>"
	for bat in batteries:
		respstr += "<li>"
		respstr += "<b>%s</b>: status is %s (%d%%)"%(bat.name, str(bat.status), bat.level)
		respstr += ", remaining time is " + (("%s (%d seconds)"%bat[3:5]) if (bat.uptime is not None) else unknownstr)
		respstr += ' <font color="green">(last updated %s)</font>' % (now if not hasattr(bat, 'last_updated') else bat.last_updated)
		respstr += "</li>"
	respstr += "</ul>"

	return HttpResponse(respstr)
