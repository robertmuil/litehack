from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
	help = """
	prints hello world
	use with 'bling' option if it tantalises you
	"""


	def handle(self, *args, **options):
		if args:
			try:
				getattr(self, args[0])(list(args[1:]))
			except AttributeError:
				print self.help
		else:
			print self.help

	def handle_noargs(self, **options):
		print "Hello, World!"

	def bling(self, args):
		print 'Hello there %s' % ('<unknown>' if (args is None) or (len(args) < 1) else str(args[0]))
