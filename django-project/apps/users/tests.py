from django.test import TestCase

from .models import User


class LogoutTests(TestCase):
	def test_logout_requires_post(self):
		user = User.objects.create_user(
			username='logout-user',
			email='logout@example.com',
			password='password',
		)
		self.client.force_login(user)

		self.assertEqual(self.client.get('/en/users/logout/').status_code, 405)
		self.assertEqual(self.client.post('/en/users/logout/').status_code, 302)
