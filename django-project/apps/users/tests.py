from captcha.models import CaptchaStore
from django.test import RequestFactory
from django.test import TestCase

from .forms import LoginForm
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


class LoginCaptchaTests(TestCase):
	def test_login_form_validates_captcha_with_request_context(self):
		request = RequestFactory().post('/en/users/')
		key = CaptchaStore.generate_key()
		challenge = CaptchaStore.objects.get(hashkey=key).challenge

		form = LoginForm(
			data={
				'username': 'unknown-user',
				'password': 'wrong-password',
				'captcha_0': key,
				'captcha_1': challenge,
			},
			request=request,
		)

		form.is_valid()

		self.assertNotIn('captcha', form.errors)
		self.assertIs(form.request, request)
