from django.test import TestCase
from mentor.users.models import User 

# Create your tests here.
class UserTest(TestCase):
	def setUp(self):
		User.objects.create(first_name="foo", last_name="bar")

	def test_get_full_name(self):
		foo = User.objects.get(first_name="foo")
		self.assertEqual(foo.get_full_name(), "foo bar")

	def test_get_short_name(self):
		foo = User.objects.get(first_name="foo")
		self.assertEqual(foo.get_short_name(), "f bar")

	def test_has_perm(self):
		foo = User.objects.get(first_name="foo")
		self.assertTrue(foo.has_perm("foo"))

	def test_has_module(self):
		foo = User.objects.get(first_name="foo")
		self.assertTrue(foo.has_module_perms("foo"))

	def test_is_student(self):
		foo = User.objects.get(first_name="foo")

		# do it twice to test cache
		self.assertTrue(foo.is_student)
		self.assertTrue(foo.is_student)

	def test_is_staff(self):
		foo = User.objects.get(first_name="foo")

		# do it twice to test cache
		self.assertFalse(foo.is_staff)
		self.assertFalse(foo.is_staff)