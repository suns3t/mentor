from django.contrib import admin
from mentor.questionaire.models import Questionaire

class QuestionaireAdmin(admin.ModelAdmin):
	# This changes QuestionaireAdmin list form
	list_display = ('student_name', 'mentor_name', 'created_on')
	list_filter = ['created_on','user']
	ordering = ['created_on']
	
	# This changes QuestionaireAdmin detail form
	fieldsets = [
		('Student and Mentor information',	{'fields':	['student_name', 'mentor_name', 'identity']}),
		('Student concern',					{'fields': 	['primary_concern', 'step_taken', 'support_from_MAPS']}),
		('Following up information',		{'fields':	['follow_up_email', 'follow_up_phone', 'follow_up_appointment']}),
	]

	
# Register your models here.
admin.site.register(Questionaire, QuestionaireAdmin)