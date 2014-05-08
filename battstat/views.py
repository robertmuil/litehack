# Create your views here.
from django.http import HttpResponse
from django.utils import timezone
import hwaccess

use_direct_access = False #Allows bypassing database and hitting hw directly.
batt_update_period = 2*60*1000 #2 minutes. The time between AJAX updates of the page.

if not use_direct_access:
	from battstat.models import Batt

unknownstr = "<em>unknown</em>"

def index(request):
	"""
	This is the primary battstat page, including the fully formed HTML source and the AJAX JavaScript for
	keeping the status up to date.

	The actual battery status is retrieved from a different URL (batt_raw) to provide the interface for the AJAX
	GET. The AJAX calls pull the latest status from the batt_raw URL and replace the 'battery_enumeration' div
	block with the returned information.

	"""
	hostname = hwaccess.get_hostname()

	respstr = "<!DOCTYPE html>"
	respstr += "<html>"
	respstr += "<head>"
	respstr += "<title>Status: %s</title>" % (hostname)
	## In the following we add JavaScript to the HTML page. This includes the AJAX functionality for 
	## updating the status of the page, as well as the timer that triggers this periodically.
	## Python string formatting is used to allow clear definition of parameters, which means that
	## we need to escape curly braces (by doubling them).
	respstr += """
							<script>
							function loadXMLDoc() {{
								var xmlhttp;
								if (window.XMLHttpRequest) {{// code for IE7+, Firefox, Chrome, Opera, Safari
									xmlhttp=new XMLHttpRequest();
								}} else {{ // code for IE6, IE5
									xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
								}}
								xmlhttp.onreadystatechange=function() {{
									if (xmlhttp.readyState==4 && xmlhttp.status==200) {{
										document.getElementById("battery_enumeration").innerHTML=xmlhttp.responseText;
									}}
								}}
								xmlhttp.open("GET","batt_raw",true);
								xmlhttp.send();
							}}

							var myVar=setInterval(function(){{loadXMLDoc()}},{batt_update_period});
							function myStopFunction() {{
								clearInterval(myVar);
							}}
							</script>
							""".format(batt_update_period=batt_update_period)

	respstr += "</head>"
	respstr += "<body>"

	nowstr = str(timezone.now())

	on_ac = False
	if use_direct_access:
		on_ac = hwaccess.on_ac()
	else:
		on_ac = hwaccess.on_ac() #TODO: store and pull ac adapter status from database

	## Now we just add some basic information to the HTML...
	respstr += "<h1>Welcome to <b>%s</b></h1>" % (hostname)
	respstr += "<p>Time now is %s</p>" % (nowstr)
	respstr += "<p>AC is %s</p>" % ("Connected" if on_ac else "Disconnected")
	respstr += "<h2>Battery Status</h2>"

	## And here is the battery status section, wrapped in a named div block to allow AJAX updating.
	respstr += '<div id="battery_enumeration">'
	respstr += get_batt_html()
	respstr += "</div>"
	#respstr += '<button type="button" onclick="loadXMLDoc()">Update Battery Status</button>'
	respstr += "</body></html>"

	return HttpResponse(respstr)

def get_batt_html():
	if use_direct_access:
		batteries = hwaccess.batteries()
	else:
		batteries = Batt.objects.all()

	respstr = "<ul>"
	for bat in batteries:
		respstr += "<li>"
		respstr += "<b>%s</b>: status is %s (%d%%)"%(bat.name, str(bat.status), bat.level)
		respstr += ", remaining time is " + (("%s (%d seconds)"%bat[3:5]) if (bat.uptime is not None) else unknownstr)
		respstr += ' <font color="green">(last updated %s)</font>' % (now if not hasattr(bat, 'last_updated') else bat.last_updated)
		respstr += "</li>"
		respstr += "</ul>"

	return respstr

def batt_raw(request):
	return HttpResponse(get_batt_html())
