from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic # For generic views.
from django.utils import timezone # To get time.

from .models import Question, Choice
# from django.template import loader -- No longer needed



# Create your views here.

# def index(request):
# 	latest_question_list = Question.objects.order_by('-pub_date')[:5]
# 	context = {
# 		'latest_question_list' : latest_question_list,
# 	}
# 	return render(request, 'polls/index.html', context)

class IndexView(generic.ListView):
	# By default ListView generic view uses template as:- 
	#		-	<appname>/<model_name>_list.html   i.e, =='polls/question_list.html'==
	# So, we tell Django to use specific template by using -- 'template_name' variable
	template_name = 'polls/index.html'

	# ListView generic view creates automatic context variable by looking at
	# Model(Question) name we have given, and make it like: question_list
	# To override this, we used - 'context_object_name' variable to use 'latest_question_list'
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		''' Return the last five published questions (not including those set to be published
		in the future )'''
		#return Question.objects.order_by('-pub_date')[:5]
		return Question.objects.filter(pub_date__lte = timezone.now()).order_by('-pub_date')[:5]


# def detail(request, question_id):
# 	question = get_object_or_404(Question, pk=question_id)
# 	return render(request, 'polls/detail.html', {'question' : question})
class DetailView(generic.DetailView):
	# DetailView can determine what is context variable for this View,
	# by looking at Model Name we provided
	model = Question
	
	# By default DetailView uses template called :-
	#		<appname>/<model_name>_detail.html i.e =='polls/question_detail.html'==
	# So, we tell Django to use specific template by using -- 'template_name' variable
	template_name = 'polls/detail.html'


# def results(request, question_id):
# 	question = get_object_or_404(Question, pk=question_id)
# 	return render(request, 'polls/results.html', {'question': question,})
class ResultsView(generic.DetailView):
	# DetailView can determine what is context variable for this View,
	# by looking at Model Name we provided
	model = Question

	# By default DetailView uses template called :-
	#		<appname>/<model_name>_detail.html i.e =='polls/question_detail.html'==
	# So, we tell Django to use specific template by using -- 'template_name' variable
	template_name = 'polls/results.html'




def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)

	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
		print(selected_choice)
	except(KeyError, Choice.DoesNotExist):
		# Redisplay the voting form
		return render(request, 'polls/detail.html', {
			'question' : question,
			'error_message': "You didn't select a choice.",
			})
	else:
		selected_choice.votes += 1 # Incrementing the vote value in DB by 1.
		selected_choice.save()
		# Always return an HttpResponseRedirect after succesfully dealing with
		# POST data. This prevents data from being posted twice if a
		# user hits the back button
		return HttpResponseRedirect(reverse('polls:results', args=(question.id, )))