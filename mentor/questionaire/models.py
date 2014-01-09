from django.db import models
from mentor.users.models import User

class Questionaire(models.Model):
	questionaire_id = models.AutoField(primary_key=True)
	created_on = models.DateTimeField(auto_now_add=True)

	# User
	user = models.ForeignKey(User)

	STUDENT = 'ST'
	MENTOR = 'MT'
	IDENTITY_CHOICES = (
		(STUDENT, 'Student'),
		(MENTOR, 'Mentor'),
	)

	# Questions
	student_name = models.CharField(max_length=30, blank=False)	# Student name
	mentor_name = models.CharField(max_length=30, blank=True)		# Mentor name
	identity = models.CharField(max_length=2,						# Are you a Student or mentor(choice field/auto)
								choices=IDENTITY_CHOICES,
								default=STUDENT)
	primary_concern = models.TextField(blank=False)					# What are your primary concerns?
	step_taken = models.TextField(blank=True)						# Please share the steps you've taken to address these concerns (if any)
	support_from_MAPS = models.TextField(blank=True)				# What kind of support would be helpful from the MAPS team?
	
	EMAIL ='EMAIL'
	PHONE = 'PHONE'
	APPOINTMENT ='APPOINT'

	FOLLOW_UP_METHOD_CHOICES = (
		(EMAIL, 'Email'),
		(PHONE, 'Phone'),
		(APPOINTMENT, 'Appointment'),
	)
	
	follow_up_method = models.CharField(max_length=20,
										choices=FOLLOW_UP_METHOD_CHOICES,
										default=EMAIL)
	class Meta:
		db_table = 'questionaire'
		