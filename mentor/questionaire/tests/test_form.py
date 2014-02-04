from mentor.questionaire.tests import UserLogin, AdminLogin
from mentor.questionaire.forms import QuestionaireForm, DownloadResponseForm
from datetime import date, timedelta 
from mentor.users.models import User 
from mentor.questionaire.models import Questionaire

class QuestionaireFormTest(UserLogin):
    def test_mentor_is_not_required(self):
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

        form = QuestionaireForm(data)
        self.assertTrue(form.is_valid())

    def test_follow_up_appoinment_in_past(self):
        data = {
            'student_name' : 'Student Name',
            'identity' : 'ST',
            'primary_concern' : 'My primary concern',
            'step_taken' : 'My steps taken',
            'support_from_MAPS' : 'Support from MAPS',
            'follow_up_email' :'abc@mail.com',
            'follow_up_phone' : '4443332222',
            'follow_up_appointment' : date.today() - timedelta(days=1),
        }

        form = QuestionaireForm(data)
        self.assertFalse(form.is_valid())

    def test_at_lest_one_follow_up_method(self):
        data = {
            'student_name' : 'Student Name',
            'identity' : 'ST',
            'primary_concern' : 'My primary concern',
            'step_taken' : 'My steps taken',
            'support_from_MAPS' : 'Support from MAPS',
        }

        form = QuestionaireForm(data)
        self.assertFalse(form.is_valid())

    def test_save(self):
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
        form.save(self.user)
        self.assertTrue(Questionaire.objects.filter(user=self.user))

class DownloadResponseFormTest(AdminLogin):
    def test_clean(self):
        data = {
            'start_date' : date.today(),
            'end_date' : date.today() - timedelta(days=1),
        }

        form = DownloadResponseForm(data)
        self.assertFalse(form.is_valid())

    def test_empty_date(self):
        data = {}

        form = DownloadResponseForm(data)
        self.assertFalse(form.is_valid())