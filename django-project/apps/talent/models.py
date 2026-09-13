from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import AuditModel, CodeGenerationModel


class TalentProfile(AuditModel):
    class Availability(models.TextChoices):
        AVAILABLE = 'available', _('Available')
        PART_TIME = 'part_time', _('Part time')
        UNAVAILABLE = 'unavailable', _('Unavailable')

    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='talent_profile',
        verbose_name=_('Owner'),
    )
    headline = models.CharField(max_length=200, verbose_name=_('Headline'))
    bio = models.TextField(blank=True, verbose_name=_('Biography'))
    phone = models.CharField(max_length=30, blank=True, verbose_name=_('Phone'))
    email = models.EmailField(blank=True, verbose_name=_('Email'))
    location = models.CharField(max_length=200, blank=True, verbose_name=_('Location'))
    skills = models.TextField(blank=True, help_text=_('Comma-separated skills.'), verbose_name=_('Skills'))
    experience_years = models.PositiveSmallIntegerField(default=0, verbose_name=_('Years of Experience'))
    availability = models.CharField(max_length=20, choices=Availability.choices, default=Availability.AVAILABLE)
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))

    class Meta:
        ordering = ['headline']
        verbose_name = _('Talent Profile')
        verbose_name_plural = _('Talent Profiles')

    def __str__(self):
        return f'{self.owner.get_full_name() or self.owner.username} - {self.headline}'


class TalentOpportunity(AuditModel, CodeGenerationModel):
    class OpportunityType(models.TextChoices):
        FULL_TIME = 'full_time', _('Full time')
        PART_TIME = 'part_time', _('Part time')
        CONTRACT = 'contract', _('Contract')
        PROJECT = 'project', _('Project')

    class Status(models.TextChoices):
        DRAFT = 'draft', _('Draft')
        OPEN = 'open', _('Open')
        CLOSED = 'closed', _('Closed')

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='talent_opportunities',
        verbose_name=_('Posted By'),
    )
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    organization_name = models.CharField(max_length=200, verbose_name=_('Organization Name'))
    description = models.TextField(verbose_name=_('Description'))
    opportunity_type = models.CharField(max_length=20, choices=OpportunityType.choices, default=OpportunityType.FULL_TIME)
    location = models.CharField(max_length=200, blank=True, verbose_name=_('Location'))
    contact_email = models.EmailField(blank=True, verbose_name=_('Contact Email'))
    contact_phone = models.CharField(max_length=30, blank=True, verbose_name=_('Contact Phone'))
    deadline = models.DateField(blank=True, null=True, verbose_name=_('Application Deadline'))
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Talent Opportunity')
        verbose_name_plural = _('Talent Opportunities')

    def __str__(self):
        return self.title


class TalentApplication(AuditModel):
    class Status(models.TextChoices):
        SUBMITTED = 'submitted', _('Submitted')
        REVIEWING = 'reviewing', _('Reviewing')
        ACCEPTED = 'accepted', _('Accepted')
        REJECTED = 'rejected', _('Rejected')

    opportunity = models.ForeignKey(TalentOpportunity, on_delete=models.CASCADE, related_name='applications')
    talent = models.ForeignKey(TalentProfile, on_delete=models.CASCADE, related_name='applications')
    cover_note = models.TextField(blank=True, verbose_name=_('Cover Note'))
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SUBMITTED)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['opportunity', 'talent'], name='unique_talent_application'),
        ]
        ordering = ['-created_at']
        verbose_name = _('Talent Application')
        verbose_name_plural = _('Talent Applications')

    def __str__(self):
        return f'{self.talent} - {self.opportunity}'