from django.shortcuts import render, get_object_or_404
from mentor.questionaire.models import Questionaire
from mentor.users.models import User 
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import QuestionaireForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def add_questionaire(request):
	"""
	This add_questionaire view is to add a new response of the questionaire
	into questionaire table
	"""

	if request.POST:
		form = QuestionaireForm(request.POST)
		if form.is_valid():
			questionaire = form.save(request.user)

			# try:
			# 	user = User.objects.get(username=request.user)
			# except User.DoesNotExist as e:
			# 	user = User.objects.create_user(request.user, '')

			# user.questionaire = questionaire
			# user.save()
			
			messages.success(request, "Questionaire response is saved")
			return HttpResponseRedirect(reverse("questionaire-adding"))
	else:
		form = QuestionaireForm()

	return render(request, "questionaire/add_questionaire.html", {
		"form" : form
	})