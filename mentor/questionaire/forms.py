from django import forms
from mentor.questionaire.models import Questionaire

class DeletableModelForm(forms.ModelForm):
	"""
	This forms has a do_delete field which is checked when the modelform is saved. 
	If it is true, the model instance is deleted and save with new value
	"""

	do_delete = forms.BooleanField(required=False, initial=False, label="Delete")

	def __init__(self, *args, **kwargs):
		super(DeletableModelForm, self).__init__(*args, **kwargs)
		# If we are adding a new model (the instance.pk will be None), then
		# there is no reason to have a delete option, since the object hasn't been
		# created yet

		if self.instance.pk is None:
			self.fields.pop("do_delete")

	def save(self, *args, **kwargs):
		if self.cleaned_data.get('do_delete'):
			self.instance.delete()
		else:
			super(DeletableModelForm, self).save(*args, **kwargs)

class QuestionaireForm(DeletableModelForm):
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