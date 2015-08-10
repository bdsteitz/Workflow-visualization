from django.db import models

# Create your models here.


'''
appt date|column id|MRN|time stamp of action|action code|display text|addl text|appt idno|racfid|full name
'''
class Task(models.Model):
	appt_date = models.DateField(db_index=True)
	column_id = models.IntegerField(db_index=True)
	mrn = models.IntegerField()
	action_dt = models.DateTimeField(db_index=True)
	action_code = models.CharField(max_length=16)
	display_text = models.CharField(max_length=128)
	addl_text = models.CharField(max_length=128, db_index=True)
	appt_idno = models.IntegerField()
	racfid = models.CharField(max_length=32)
	full_name = models.CharField(max_length=128)
	

