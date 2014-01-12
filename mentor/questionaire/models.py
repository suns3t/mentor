from django.db import models
from django import forms
from mentor.users.models import User

class Questionaire(models.Model):
	questionaire_id = models.AutoField(primary_key=True)
	created_on = models.DateTimeField(auto_now_add=True)


	STUDENT = 'ST'
	MENTOR = 'MT'
	IDENTITY_CHOICES = (
		(STUDENT, 'Student'),
		(MENTOR, 'Mentor'),
	)

	# User submited this form
	user = models.ForeignKey(User)

	# Questions
	student_name = models.CharField(max_length=30, blank=False)	# Student name
	mentor_name = models.CharField(max_length=30, blank=True)		# Mentor name
	identity = models.CharField(max_length=2,						# Are you a Student or mentor(choice field/auto)
								choices=IDENTITY_CHOICES,
								default=STUDENT)
	primary_concern = models.TextField(blank=False)					# What are your primary concerns?
	step_taken = models.TextField(blank=True)						# Please share the steps you've taken to address these concerns (if any)
	support_from_MAPS = models.TextField(blank=True)				# What kind of support would be helpful from the MAPS team?
	
	follow_up_method = models.CharField(max_length=20, blank=True)
	class Meta:
		db_table = 'questionaire'
		