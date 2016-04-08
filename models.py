from django.db import models
from django.contrib.auth.models import User 

class profile(models.Model):	
	branch=models.IntegerField(default=0)
	mob_no=models.IntegerField(default=0)
	user=models.ForeignKey(User)
	#email=models.CharField(max_length=300)
	leaves_left=models.IntegerField(default=10)

class application(models.Model):
	datefrom=models.CharField(max_length=40)
	dateto=models.CharField(max_length=40)
	reason=models.CharField(max_length=300)
	proxy=models.CharField(max_length=200,default=0)
	type_leave=models.IntegerField() #1 for casual, 2 medical
	user=models.ForeignKey(User)
	status=models.IntegerField() # 0-pending 1-accpeted 2-rejected
	branch=models.IntegerField(default=0) #1 for comp,2 for it , 3 entc 4 Applied Science
# Create your models here.
