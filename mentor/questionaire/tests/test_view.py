from mentor.questionaire.tests import InitQuestionaire
from mentor.questionaire.models import Questionaire
from django.test import TestCase
from django.test.client import Client 
from django.core.urlresolvers import reverse
from datetime import date 

class QuestionaireViewTest(InitQuestionaire):
	def test_get(self):
		response = self.client.get(reverse('questionaire-adding'))
		self.assertEqual(response.status_code, 200)

	def test_post(self):
		data = {
			'student_name' : 'Student Name',
			'identity' : 'ST',
			'primary_concern' : 'My primary concern',
			'step_taken' : 'My steps taken',
			'support_from_MAPS' : 'Support from MAPS',
			'follow_up_email' :'abc@mail.com',
			'follow_up_phone' : '4443332222',
			'follow_up_appoinment' : date.today(),
		}

		response = self.client.post(reverse('questionaire-adding'), data)
		# Make sure the save method is called
		self.assertTrue(Questionaire.objects.filter(student_name=data['student_name']).exists())
		self.assertRedirects(response, reverse('questionaire-thanks'))