from django.shortcuts import render, get_object_or_404
from mentor.questionaire.models import Questionaire
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import QuestionaireForm

# Create your views here.

def edit_questionaire(request, questionaire_id):
	"""
	This edit_questionaire view is to edit an exist response of the questionaire
	submited by student or mentor on behalf of student
	"""
	questionaire = get_object_or_404(Questionaire, questionaire_id=questionaire_id)
	if request.POST:
		form = QuestionaireForm(request.POST, instance=questionaire)
		if form.is_valid():
			messages.success(request, "Questionaire response is edit")
			return HttpResponseRedirect(reverse("questionaire_editing", args=(questionaire.pk,)))

	else:
		form = QuestionaireForm(instance=questionaire)

	return render(request, "questionaire/edit_questionaire.html", {
		"questionaire" : questionaire,
		"form" : form
	})

def add_questionaire(request):
	"""
	This add_questionaire view is to add a new response of the questionaire
	into questionaire table
	"""

	if request.POST:
		form = QuestionaireForm(request.POST)
		if form.is_valid():
			messages.success(request, "Questionaire response is saved")
			return HttpResponseRedirect(reverse("questionaire_adding"))
	else:
		form = QuestionaireForm()

	return render(request, "questionaire/add_questionaire.html", {
		"form" : form
	})

def listing(request):
	""" 
	List all the reponses that the user can edit/delete or add new response
	"""
	questionaires = Questionaire.objects.all()
	return render(request, "questionaire/listing.html", {
		"questionaires" : questionaires
	})

def detail(request, questionaire_id):
	questionaire = get_object_or_404(Questionaire, questionaire_id=questionaire_id)

	return render(request, "questionaire/detail.html", {
		"questionaire" : questionaire
	})