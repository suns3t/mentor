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
from django.utils.timezone import localtime
from mentor.utils import UnicodeWriter
import pytz
from django.conf import settings
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
            form.save(request.user)

            return HttpResponseRedirect(reverse('questionaire-thanks'))
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
            #import pdb; pdb.set_trace()
            end_date = form.cleaned_data['end_date'] + timedelta(days=1)

            filename = "Report Responses from " + start_date.strftime("%Y-%m-%d") + " to " + end_date.strftime("%Y-%m-%d")
            
            our_timezone = pytz.timezone(settings.TIME_ZONE)
            start_date_tz = our_timezone.localize(datetime.combine(start_date, datetime.min.time()))
            end_date_tz = our_timezone.localize(datetime.combine(end_date, datetime.min.time()))

            questionaires = Questionaire.objects.filter(created_on__lt=end_date_tz,created_on__gte=start_date_tz)

            http_response = HttpResponse()
            http_response = HttpResponse(content_type='text/csv')
            http_response['Content-Disposition'] = 'attachment; filename="%s.csv"' % (filename)

            writer = UnicodeWriter(http_response)
            header = ["submitted on", "odin name", "student name", "student_ID" ,"mentor name", "identity" , "on_behalf_of_student" , "primary_concern", "step_taken", "when_take_step" ,"support_from_MAPS", "contact_who", "follow_up_email", "follow_up_phone", "follow_up_appointment"]
            writer.writerow(header)
            
            for questionaire in questionaires:
                csv_row = []
                csv_row.append(localtime(questionaire.created_on).strftime("%Y-%m-%d %H:%M:%S"))
                csv_row.append(questionaire.user.username)
                csv_row.append(questionaire.student_name)
                csv_row.append(str(questionaire.student_ID))
                csv_row.append(questionaire.mentor_name)
                csv_row.append(questionaire.identity)
                csv_row.append(questionaire.on_behalf_of_student)
                csv_row.append(' ,'.join([str(primary_concern) for primary_concern in questionaire.primary_concern.all ]))
                csv_row.append(questionaire.primary_concern_other)
                csv_row.append(questionaire.step_taken)
                csv_row.append(questionaire.when_take_step)
                csv_row.append(questionaire.support_from_MAPS)
                csv_row.append(questionaire.contact_who)
                csv_row.append(questionaire.follow_up_email)
                csv_row.append(str(questionaire.follow_up_phone))

                writer.writerow(csv_row)

            return http_response
    else:
        form = DownloadResponseForm()

    return render(request, "admin/download_csv.html", {
        "form" : form,
        "title" : title,
    })