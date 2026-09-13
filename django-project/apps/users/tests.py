from captcha.models import CaptchaStore
from django.test import RequestFactory
from django.test import TestCase
from django.urls import reverse

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


class BackendStateHomeTests(TestCase):
	def test_home_requires_login(self):
		response = self.client.get(reverse('users:home'))

		self.assertRedirects(response, f"{reverse('users:login')}?next={reverse('users:home')}")

	def test_home_lists_backend_state_views(self):
		user = User.objects.create_user(
			username='backend-user',
			email='backend@example.com',
			password='password',
		)
		self.client.force_login(user)

		response = self.client.get(reverse('users:home'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, reverse('news:news-list'))
		self.assertContains(response, reverse('market:updates'))
		self.assertContains(response, reverse('supply:center'))
		self.assertContains(response, reverse('talent:center'))
