from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import TalentApplication, TalentOpportunity, TalentProfile


class TalentModelTests(TestCase):
    def test_talent_application_connects_profile_and_opportunity(self):
        user = get_user_model().objects.create_user(
            username='talent-owner',
            email='talent@example.com',
            password='password',
        )
        profile = TalentProfile.objects.create(owner=user, headline='Product Designer')
        opportunity = TalentOpportunity.objects.create(
            owner=user,
            title='Design local marketplace',
            organization_name='Lao Product',
            description='Improve the shopping experience.',
            status=TalentOpportunity.Status.OPEN,
        )

        application = TalentApplication.objects.create(
            opportunity=opportunity,
            talent=profile,
            cover_note='I would like to help.',
        )

        self.assertEqual(opportunity.applications.get(), application)
        self.assertEqual(profile.applications.get(), application)