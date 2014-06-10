from permissions import permission
from .models import User
from mentor.questionaire.models import Questionaire

@permission
def can_view_mentor_homepage(user):
    return user.is_staff or user.is_mentor

@permission
def can_view_response_detail(user, response_id):
    response = Questionaire.objects.get(pk=response_id)

    return response.user==user or user.is_staff or user.is_mentor

@permission
def can_resolve_response(user, response_id):
    return user.is_mentor or user.is_staff