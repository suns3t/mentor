from django.test import TestCase
from mentor.questionaire.models import Questionaire 
from mentor.users.models import User 

class InitQuestionaire(TestCase):

	def setUp(self):
		super(InitQuestionaire, self).setUp()

		self.user = User(username='foo', first_name='Foo', last_name='Bar',email='whatever@mail.com')
		self.user.set_password('foo')
		self.user.is_staff = 1
		self.user.save()

		self.assertTrue(self.client.login(username=self.user.username, password='foo'))