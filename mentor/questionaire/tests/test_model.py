from mentor.questionaire.tests import UserLogin, AdminLogin
from mentor.questionaire.models import Questionaire
from mentor.users.models import User
from datetime import date 
# Create your tests here.
class QuestionaireModelTest(UserLogin):
	def test_sendNotification(self):
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
		out = questionaire.sendNotification()

		# Make sure that 2 emails are sent, one to user, one to staff-group
		self.assertEqual(out, 2)
