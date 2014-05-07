from django.db import models

# Create your models here.
class Batt(models.Model):
	name = models.CharField(max_length=200,unique=True)
	level = models.IntegerField(blank=True,null=True)
	status = models.CharField(max_length=200,blank=True,null=True)
	uptime = models.CharField(max_length=200,blank=True,null=True)
	str_uptime = models.CharField(max_length=200,blank=True,null=True)
	last_updated = models.DateTimeField('date updated',auto_now=True)

	def __unicode__(self):
		retstr = '%s'%(self.name)
		if self.level is not None:
			retstr += '@ %d%%'%(self.level)
		if self.status is not None:
			retstr += ', %s' % (self.status)
		if self.last_updated is not None:
			retstr += ' (last updated %s)'%(self.last_updated)

		return retstr

	def is_full(self):
		return self.level > 99
