from django.shortcuts import render
from mentor.questionaire.models import Questionaire
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

# Create your views here.
def mentor_home(request):
    responses = Questionaire.objects.all()

    return render(request, "mentor/home.html", {
        "responses" : responses,
    })