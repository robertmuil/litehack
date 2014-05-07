"""
Very simple interface to grab hardware information.

This just abstracts the actual access to low-level system so that other
modules in the web stack can just rely on this.

This will use the acpi python module, but actually is capable for the most
part of just accessing the /sys/classes mountpoints directly if access
to the acpi binary is not available on the system.

On older systems, the /proc/acpi mount-point may be used, but this has been obsoleted.

Author: robertmuil

"""

import os, socket
import subprocess
from pythonacpi import acpi #this is a helper package to parse the 'acpi' binary's output (https://github.com/ondrejsika/python-acpi - it's also in PyPI)

use_acpi_binary = True

#Standard ACPI path is /sys/class/power_supply
ps_path = os.path.join('/sys', 'class', 'power_supply')
ac_path = os.path.join(ps_path,'AC', 'online')

def get_hostname():
	return socket.gethostname()

def on_ac():
	"""
	Determines if the AC adapter is plugged in or not.
	"""
	ac = False
	if use_acpi_binary:
		ac = acpi.on_ac()
	else:
		with open(ac_path, 'r') as ac_file:
			ac_state = ac_file.read()
			#print '%s: "%s"'%(ac_file.name, ac_state)
			ac = (ac_state[0] == '1')

	return ac

def batteries():
	"""
	Returns batteries as retrieved from ACPI or system class path.

	Will return a named tuple if requested, and this is false only for legacy reasons.

	TODO: add non acpi_binary version
	"""
	if use_acpi_binary:
		batts = acpi.batteries()
	else:
		raise NotImplementedError
		batt_status_path = os.path.join(ps_path, 'BAT%d'%(batt_num), 'status')
		with open(batt_status_path, 'r') as f:
			batt_status = f.read()
			status_string = batt_status

	return batts

def adapters():
	"""
	TODO: add non acpi_binary version
	"""
	if use_acpi_binary:
		res = acpi.adapters()
	else:
		raise NotImplementedError

	return res
