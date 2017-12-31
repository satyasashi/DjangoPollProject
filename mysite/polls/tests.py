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