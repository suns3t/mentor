from permissions import permission
from .models import User

@permission
def can_view_mentor_homepage(user):
    return user.is_staff or user.is_mentor