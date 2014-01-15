from django import forms
from mentor.questionaire.models import Questionaire
import datetime

class QuestionaireForm(forms.ModelForm):

	STUDENT = 'ST'
	MENTOR = 'MT'
	IDENTITY_CHOICES = (
		(STUDENT, 'Student'),
		(MENTOR, 'Mentor'),
	)
	student_name = forms.CharField(error_messages={'required':'Please enter student name'})
	
	identity = forms.ChoiceField(
		choices=IDENTITY_CHOICES,
		label='Are you a student or a mentor?')
	
	primary_concern = forms.CharField(
		widget=forms.widgets.Textarea,
		label='What are your primary concerns?')
	
	step_taken = forms.CharField(
		widget=forms.widgets.Textarea,
		label="Please share the steps you've taken to address these concerns (if any)")

	support_from_MAPS = forms.CharField(
		widget=forms.widgets.Textarea,
		label="What kind of support did you receive from MAPS before?")
	follow_up_email = forms.EmailField(
		widget=forms.widgets.EmailInput,
		label='Email')
	follow_up_phone = forms.CharField(
		error_messages={'required':'Please insert an appropriate phone number'},
		widget=forms.widgets.TextInput,
		label='Phone call')
	follow_up_appointment = forms.DateField(
		label='Personal meeting on')

	def save(self, user, *args, **kwargs):
		"""
		Overide the save method to input username automatically from
		CAS authentication information
		"""

		self.instance.user = user
		post = super(QuestionaireForm, self).save(*args, **kwargs)
		post.save()

	def clean(self):
		cleaned_data = super(QuestionaireForm, self).clean()

		# Make sure that user enters at least one method of follow-up
		email = cleaned_data.get("follow_up_email")
		phone = cleaned_data.get("follow_up_phone")
		appointment = cleaned_data.get("follow_up_appointment")

		import pdb; pdb.set_trace();
		if email is None and appointment is None and phone is None :
			raise forms.ValidationError('Fill at least one method to follow-up you')
		return cleaned_data
	class Meta:
		model = Questionaire 
		fields = (
			'student_name',
			'mentor_name',
			'identity',
			'primary_concern',
			'step_taken',
			'support_from_MAPS',
			'follow_up_email',
			'follow_up_phone',
			'follow_up_appointment',
		)