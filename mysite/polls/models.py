import datetime
from django.db import models
from django.utils import timezone

# Create your models here.
class Question(models.Model):
	question_text	=	models.CharField(max_length=200)
	pub_date		=	models.DateTimeField('date_published')

	def __str__(self):
		return self.question_text

	# Checks if post published >= yesterday
	def was_published_recently(self):
		#return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
		# As above time calculation is a Bug for future timing.
		# i.e. was_published_recently() is also being true for future published
		# which is not possible.

		'''Here is how it works:
			- Works on Published Date, Yesterday, Today
			- which makes sure Publishment was RECENT (only 1day and today) not in 'Future'
			- example: 					
					> yesterday = 30th
					> publishedOn = 25th
					> today(now) = 31st
					
					> 30 <= 25 <= 31 ---> 30 <= 25 is False, 
		'''
		now = timezone.now() # Present time
		yesterday = timezone.now() - datetime.timedelta(days=1) # Yesterday's time
		return yesterday <= self.pub_date <= now

class Choice(models.Model):
	question 	=	models.ForeignKey(Question, on_delete=models.CASCADE)
	choice_text	=	models.CharField(max_length=200)
	votes		=	models.IntegerField(default=0)

	def __str__(self):
		return self.choice_text