from django.shortcuts import render, get_object_or_404
from mentor.questionaire.models import Questionaire, UserResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
import datetime
from django.utils.timezone import utc 
from .perms import decorators
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
@decorators.can_view_mentor_homepage
def mentor_home(request):
    responses = Questionaire.objects.all()

    for response in responses:
        userResponses = UserResponse.objects.filter(response=response)
        response.userResponses = userResponses

    # Using Paginator from Django
    paginator = Paginator(responses, 10) # Show 10 responses per page

    page = request.GET.get('page')
    try:
        responses = paginator.page(page)
    except PageNotAnInteger:
        responses = paginator.page(1)
    except EmptyPage:
        responses = paginator.page(paginator.num_pages)

    return render(request, "mentor/home.html", {
        "responses" : responses,
    })

# Detail response for mentor to view
@decorators.can_view_response_detail
def response_detail(request, response_id):
    response = get_object_or_404(Questionaire, pk=response_id)

    try:
        # Sort in descending order the userReponses based on created_on time and get the latest item.
        response.userResponse = UserResponse.objects.filter(response=response).order_by("-created_on")[0]
    except:
        response.userResponse = None

    return render(request, "mentor/response_detail.html", {
        "response" : response,
    })
    
@decorators.can_resolve_response
def response_resolve(request, response_id):
    response = get_object_or_404(Questionaire, pk=response_id)

    try:
        userResponse = UserResponse.objects.get(response=response, mentor_resolved=request.user)
        # If userResponse does exist corresponding to this response and this user
        userResponse.status = not userResponse.status
        userResponse.created_on = datetime.datetime.utcnow().replace(tzinfo=utc)
        userResponse.save()

    except Exception, e:
        # userResponse does not exist, create a new one
        userResponse = UserResponse(response=response, mentor_resolved=request.user)
        userResponse.created_on = datetime.datetime.utcnow().replace(tzinfo=utc)
        userResponse.status = True
        userResponse.save()

    return HttpResponseRedirect(reverse('mentor-homepage'))

