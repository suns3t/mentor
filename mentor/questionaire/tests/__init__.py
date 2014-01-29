from django.test import TestCase
from mentor.questionaire.models import Questionaire 
from mentor.users.models import User 

class UserLogin(TestCase):
	def setUp(self):
		super(UserLogin, self).setUp()

		self.user = User(username='foo', first_name='Foo', last_name='Bar',email='whatever@mail.com')
		self.user.set_password('foo')
		self.user.save()

		self.assertTrue(self.client.login(username=self.user.username, password='foo'))

class AdminLogin(TestCase):
	def setUp(self):
		super(AdminLogin, self).setUp()

		self.user = User(username='admin', first_name='Admin', last_name='ABC',email='whatever@mail.com')
		self.user.set_password('admin')
		self.is_staff = 1
		self.user.save()

		self.assertTrue(self.client.login(username=self.user.username, password='admin'))