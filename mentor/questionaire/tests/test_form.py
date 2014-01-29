from mentor.questionaire.tests import InitQuestionaire
from mentor.questionaire.forms import QuestionaireForm
from datetime import date 

class QuestionaireFormTest(InitQuestionaire):
	def test_mentor_is_not_required(self):
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

		form = QuestionaireForm(data)
		self.assertTrue(form.is_valid())