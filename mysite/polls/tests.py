import datetime

from django.utils import timezone
from django.test import TestCase

# To avoid hardcoded urls, we use reverse to get url by 'name'
# of url() attribute.
from django.urls import reverse 

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
		# Future question -> Created a question 30 days in future
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

	def create_question(question_text, days):
		"""
			Create a question with the given 'question_text' and published the
			given number of `days` offset to now (negative for questions published
			in the past, Positive for questions that have yet to be published).
		"""
		time = timezone.now() + datetime.timedelta(days=days)
		return Question.objects.create(question_text=question_text, pub_date=time)



class QuestionIndexViewTests(TestCase):
	def test_no_questions(self):
		"""
		If no questions exist, an appropriate message is displayed.
		"""

		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No polls are available.")
		self.assertQuerysetEqual(response.context['latest_question_list'], [])

	def test_past_question(self):
		"""
		Questions with a pub_date  in the past are displayed on the 
		Index page
		"""
		create_question(question_text="Past question.", days=-30)
		response = self.client.get(reverse('polls:index'))

		"""As we used our custom create function to create
		a Question -> Past question, we check if context of 
		'latest_question_list' if it has 'Past question'
        """
        self.assertQuerysetEqual(
        	response.context['latest_question_list'],['<Question: Past question.>']
        	)
    def test_future_question(self):
    	"""
		Questions with a pub_date in the future aren't displayed on the index page
    	"""
    	create_question(question_text="Future question.", days=30)
    	response = self.client.get(reverse('polls:index'))
    	self.assertContains(response, "No polls are available.")

    	self.assertQuerysetEqual(response.context['latest_question_list'], [])