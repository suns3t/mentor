from mentor.questionaire.tests import UserLogin, AdminLogin
from mentor.questionaire.models import Questionaire
from django.test import TestCase
from django.test.client import Client 
from django.core.urlresolvers import reverse
from datetime import date 

# Test add_questionaire view
class QuestionaireViewTest(UserLogin):
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
			'follow_up_appointment' : date.today(),
		}

		response = self.client.post(reverse('questionaire-adding'), data)
		# Make sure the save method is called
		self.assertTrue(Questionaire.objects.filter(student_name=data['student_name']).exists())
		self.assertRedirects(response, reverse('questionaire-thanks'))

# Test report view
class ReportViewTest(AdminLogin):
	def test_get(self):
		response = self.client.get(reverse('questionaire-reporting'))
		self.assertEqual(response.status_code, 200)

	def test_post(self):

		# Create a database
		questionaire = Questionaire(
			student_name='Student Name',
			identity='ST',
			primary_concern='My primary concern',
			step_taken='My steps taken',
			support_from_MAPS='Support from MAPS',
			follow_up_email='abc@mail.com',
			follow_up_phone='4443332222',
			follow_up_appointment=date.today(),
		)
		questionaire.user = self.user 
		questionaire.save()

		data = {
			'start_date' : date.today(),
			'end_date' : date.today(),
		}

		response = self.client.post(reverse('questionaire-reporting'), data)
		# Need to test csv reponse
		self.assertTrue(response)