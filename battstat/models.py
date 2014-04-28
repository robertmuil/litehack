from django.db import models

# Create your models here.
class Batt(models.Model):
	name = models.CharField(max_length=200)
	mfr_date = models.DateTimeField('date manufactured')

	def __unicode__(self):
		return '%s (%s)'%(self.name, self.mfr_date)

#This isn't the best way to do this... we don't need to presere this
# information
class Status(models.Model):
	batt = models.ForeignKey(Batt)
	status_text = models.CharField(max_length=200)
	percent_full = models.IntegerField(default=0)

	def __unicode__(self):
		return 'status of %s: %d%% (%s)'%(self.batt.name, self.percent_full, self.status_text)

	def is_full(self):
		return self.percent_full > 99
