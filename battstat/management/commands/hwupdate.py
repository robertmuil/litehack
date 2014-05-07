"""

TODO: allow manipulation of update frequency (which could then be set as the lowest possible to service all client requests)
TODO: 

Author: robertmuil
"""
import logging
import glob
import logging.handlers

from time import sleep

from django.core.management.base import BaseCommand
from django.db import transaction
from battstat.models import Batt
from django.core.exceptions import ObjectDoesNotExist

from pythonacpi import acpi

LOG_FILENAME = 'hwupdate.log'
UPDATE_PERIOD = 0.5

# Set up a specific logger with our desired output level
log = logging.getLogger('hwupdate')
log.setLevel(logging.DEBUG)
handler = logging.handlers.RotatingFileHandler(
              LOG_FILENAME, maxBytes=1024*1024*1, backupCount=5)
log.addHandler(handler)

class Command(BaseCommand):
	help = """
	Use with the following options:
		- start
		- stop
	"""

	def handle(self, *args, **options):
		if args:
			func = getattr(self, args[0], None)
			if callable(func):
				func(list(args[1:]))
			else:
				print "\nInvalid option supplied (%s)." % (args[0])
				print self.help
		else:
			print self.help

	def start(self, args):
		"""
		This function starts a loop, intended to be run in parallel to the main server process,
		to asynchronously maintain the database with up-to-date 

		The loop will iterate the entries in the maintained databases (e.g. batteries) and action them in the following way:
		 - if the entry is a known meta-command, this will be executed. These can be used to stop the looping, for example.
		 - if the entry matches a currently installed battery, this entry will be updated with the status
		 - if the entry is not a command and does not match installed batteries, it will be flagged as absent (NOT YET IMPLEMENTED)
		If any batteries are found to be present in the system and not in the database, they will be added.
		"""
		stop = False
		#enumerate_batteries()
		while not stop:
			log.debug('hwupdate running (period=%.2fsec)...'%(UPDATE_PERIOD))
			sleep(UPDATE_PERIOD)
			log.debug("Reading ACPI battery information...")
			batts = acpi.batteries()
			log.debug("...done reading ACPI (%d found)." % (len(batts)))
			battnames = [b[0] for b in batts]
			known_batts = []
			try:
				log.debug("Scanning database...")
				with transaction.commit_on_success():
					dbbatteries = Batt.objects.all()
					for dbbatt in dbbatteries:
						if dbbatt.name == 'STOP_UPDATING':
							log.info("hwupdate async task signaled to stop. Stopping.")
							stop = True
							dbbatt.delete()
						elif dbbatt.name in battnames:
							log.debug("Battery '%s' matches in ACPI and DB." % (dbbatt.name))
							hwbatt=batts[battnames.index(dbbatt.name)]
							dbbatt.status=hwbatt.status
							dbbatt.level=hwbatt.level
							dbbatt.uptime=hwbatt.uptime
							dbbatt.str_uptime=hwbatt.str_uptime
							dbbatt.save()
							log.debug(" - updating with %s/%d/%s" % (hwbatt.status, hwbatt.level, hwbatt.str_uptime))
							known_batts += [dbbatt.name]

						else:
							log.info("Battery '%s' in DB is absent in ACPI." % dbbatt.name)

				log.debug("Checking all HW batteries")
				for hwbatt in batts:
					if hwbatt[0] not in known_batts:
						log.info("Battery '%s' in ACPI is absent in DB. Adding." % hwbatt.name)
						dbbatt=Batt(name=hwbatt.name,
							level=hwbatt.level,
							status=hwbatt.status,
							uptime=hwbatt.uptime,
							str_uptime=hwbatt.str_uptime,
							)
						dbbatt.save()

				log.debug("...done scanning DataBase.")
			except Exception as ex:
				log.exception('HWUpdate got exception: %s'%str(ex))
				#TODO: implement back-off of loop delay with multiple exceptions.

	def stop(self, args):
		"""
		Writing a special entry to the table is probably not the best way to get this
		signal meta-conditions to the update thread. TODO.
		"""
		b=Batt(name='STOP_UPDATING')
		b.save()

def enumerate_batteries():
	"""
	This function enumerates the batteries on the system and creates
	an entry in the DataBase table for each.

	This is deprecated by the update loop itself.
	"""

	batts = acpi.batteries()

	for batt in batts:
		b = None
		try:
			b = Batt.objects.get(name=batt[0])
		except ObjectDoesNotExist:
			log.debug("creating new entry for '%s'"%batt[0])
		if b is None:
			b=Batt(name=batt[0],
					status_text=batt[1],
					percent_full=batt[2],
					remaining_text=batt[4],
					)
		else:
			b.status_text=batt[1]
			b.percent_full=batt[2]
			b.remaining_text=batt[4]
		b.save()
