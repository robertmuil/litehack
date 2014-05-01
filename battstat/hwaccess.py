#Very simple interface to grab hardware information
import os, socket
import subprocess
import acpi #this is just a helper package to parse the 'acpi' binary's output (https://github.com/ondrejsika/python-acpi - it's also in PyPI)

use_acpi_binary = True

#Standard ACPI path is /sys/class/power_supply
ps_path = os.path.join('/sys', 'class', 'power_supply')
ac_path = os.path.join(ps_path,'AC', 'online')

def get_hostname():
	return socket.gethostname()

def is_plugged_in():
	"""
	Determines if the AC adapter is plugged in or not.

	Doesn't use acpi binary, probably should for consistency.
	"""
	ac_plugged = False
	with open(ac_path, 'r') as ac_file:
		ac_state = ac_file.read()
		#print '%s: "%s"'%(ac_file.name, ac_state)
		ac_plugged = (ac_state[0] == '1')

	return ac_plugged

def get_batt_status(batt_num):
	"""
	This function simply returns the status_string of the battery
	named by input. Battery number is 0 or higher for extra batteries. 

	Currently, this uses the /sys/classes file-system interface. Could also use the 'acpi' package, but this typically
	requires installation on most standard linux systems. /sys/classes is standard.

	On older systems, the /proc/acpi mount-point may be used, but this has been obsoleted.

	TODO: this shouldn't do formatting, and should indicate unknown batteries through exceptions.
	"""
	status_string = "<em>unknown</em>"

	if use_acpi_binary:
		battstats = acpi.acpi()
		if len(battstats) > batt_num:
			status_string = ""
			bat = battstats[batt_num]
			status_string += "<em>%s</em> is %s (%d%%)" %bat[0:3]
			if bat[3] is not None:
				status_string += ", remaining time is %s (%d seconds)"%bat[3:5]

	else:
		batt_status_path = os.path.join(ps_path, 'BAT%d'%(batt_num), 'status')
		with open(batt_status_path, 'r') as f:
			batt_status = f.read()
			status_string = batt_status
	
	return status_string
