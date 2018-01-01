import datetime

from django.utils import timezone
from django.test import TestCase

from .models import Question # importing the models we want to test

# Create your tests here.
class QuestionModelTest(TestCase):
	def test_was_published_recently_with_future_question(self):
		"""
			was_published_recently() will return False for the questions
			whose pub_date was in future
		"""

		# Future time
		time = timezone.now() + datetime.timedelta(days=30)
		# Future question - Created a question 30 days in future
		future_question = Question(pub_date=time)
		self.assertIs(future_question.was_published_recently(), False)

	def test_was_published_recently_with_old_question(self):
		"""
			was_published_recently() returns False for questions whose
			pub_date is older than 1 Day.

		"""
		time = timezone.now() - datetime.timedelta(days=1, seconds=1)
		old_question = Question(pub_date=time)
		self.assertIs(old_question.was_published_recently(), True)

	def test_was_published_recently_with_recent_question(self):
		"""
			was_published_recently returns True whose pub_date is 
			with in last day.
		"""
		time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
		recent_question = Question(pub_date=time)
		self.assertIs(recent_question.was_published_recently(), True)