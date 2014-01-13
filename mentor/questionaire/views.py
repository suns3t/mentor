from django.shortcuts import render, get_object_or_404
from mentor.questionaire.models import Questionaire
from mentor.users.models import User 
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import QuestionaireForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from datetime import date

from mentor.utils import UnicodeWriter

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

@staff_member_required
def report(request):
	"""
	This report view is to report a csv file contains all the questionaires data
	Only can viewed by staff members
	"""

	questionaires = list(Questionaire.objects.all())
	timestamp = date.today()
	filename = "Report"

	http_response = HttpResponse()
	http_response = HttpResponse(content_type='text/csv')
	http_response['Content-Disposition'] = 'attachment; filename="%s.csv"' % (filename)

	writer = UnicodeWriter(http_response)
	header = ["student name", "mentor name", "submitted on"]
	writer.writerow(header)
	
	for questionaire in questionaires:
		csv_row = []
		csv_row.append(questionaire.student_name)
		csv_row.append(questionaire.mentor_name)
		csv_row.append(questionaire.created_on.strftime("%Y-%m-%d %H:%M:%S"))

		writer.writerow(csv_row)

	return http_response