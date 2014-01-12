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

	follow_up_method = forms.MultipleChoiceField(
		widget=forms.CheckboxSelectMultiple,
		choices=FOLLOW_UP_METHOD_CHOICES)

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
		)