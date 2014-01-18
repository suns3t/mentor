from django.shortcuts import render, get_object_or_404
from mentor.questionaire.models import Questionaire
from mentor.users.models import User 
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import QuestionaireForm, DownloadResponseForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from datetime import date, timedelta, datetime

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
	title = " Responses "
	if request.POST:
		form = DownloadResponseForm(request.POST)
		if form.is_valid():
			start_date = form.cleaned_data['start_date']
			end_date = form.cleaned_data['end_date'] + timedelta(days=1)

			questionaires = list(Questionaire.objects.filter(created_on__lt=end_date,created_on__gte=start_date))
			timestamp = datetime.today()
			filename = "Report Responses at " + timestamp.strftime("%Y-%m-%d %H:%M:%S") + " from " + start_date.strftime("%Y-%m-%d") + " to " + end_date.strftime("%Y-%m-%d")

			http_response = HttpResponse()
			http_response = HttpResponse(content_type='text/csv')
			http_response['Content-Disposition'] = 'attachment; filename="%s.csv"' % (filename)

			writer = UnicodeWriter(http_response)
			header = ["student name", "mentor name", "submitted on", "primary_concern", "step_taken", "support_from_MAPS", "follow_up_email", "follow_up_phone", "follow_up_appointment"]
			writer.writerow(header)
			
			for questionaire in questionaires:
				csv_row = []
				csv_row.append(questionaire.student_name)
				csv_row.append(questionaire.mentor_name)
				csv_row.append(questionaire.created_on.strftime("%Y-%m-%d %H:%M:%S"))
				csv_row.append(questionaire.primary_concern)
				csv_row.append(questionaire.step_taken)
				csv_row.append(questionaire.support_from_MAPS)
				csv_row.append(questionaire.follow_up_email)
				csv_row.append(questionaire.follow_up_phone)
				csv_row.append(questionaire.follow_up_appointment.strftime("%Y-%m-%d"))

				writer.writerow(csv_row)

			return http_response
	else:
		form = DownloadResponseForm()

	return render(request, "admin/download_csv.html", {
		"form" : form,
		"title" : title,
	})