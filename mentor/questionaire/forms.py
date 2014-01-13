from django import forms
from mentor.questionaire.models import Questionaire

class QuestionaireForm(forms.ModelForm):

	EMAIL ='EMAIL'
	PHONE = 'PHONE'
	APPOINTMENT ='APPOINT'

	FOLLOW_UP_METHOD_CHOICES = (
		(EMAIL, 'Email'),
		(PHONE, 'Phone'),
		(APPOINTMENT, 'Appointment'),
	)

	STUDENT = 'ST'
	MENTOR = 'MT'
	IDENTITY_CHOICES = (
		(STUDENT, 'Student'),
		(MENTOR, 'Mentor'),
	)

	follow_up_method = forms.ChoiceField(
		choices=FOLLOW_UP_METHOD_CHOICES,
		label='Contact method')
	follow_up_contact_info = forms.CharField(
		label='Contact information')
	identity = forms.ChoiceField(
		choices=IDENTITY_CHOICES,
		label='Are you a student or a mentor?')
	def save(self, user, *args, **kwargs):
		"""
		Overide the save method to input username automatically from
		CAS authentication information
		"""

		self.instance.user = user
		post = super(QuestionaireForm, self).save(*args, **kwargs)
		post.save()

	class Meta:
		model = Questionaire 
		fields = (
			'student_name',
			'mentor_name',
			'identity',
			'primary_concern',
			'step_taken',
			'support_from_MAPS',
			'follow_up_method',
			'follow_up_contact_info'
		)