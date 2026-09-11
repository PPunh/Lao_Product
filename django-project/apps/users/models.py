# coding=utf-8
from django.db import models
from django.conf import settings
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password, is_password_usable
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    '''custom user model inherited from default Django AUTH User model'''

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    phone_number = models.CharField(
        max_length=8,
        unique=True,
        null=True,
        blank=True,
        error_messages={"unique": "A user with that phone number already exists.",},
    )

    # make email field to be unique, default django auth allow duplicated email address
    email = models.EmailField(
        max_length=60,
        unique=True,
        error_messages={"unique": "A user with that email address already exists.",},
    )

    # now when create an user account, it requires email too. Note: username is always required by Django
    REQUIRED_FIELDS = ["email"]
    date_modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='modified_users'
    )

    def save(self, *args, request=None, **kwargs):
        '''
        Custom save method to handle date/time update,
        and setting the 'modified_by' field.
        '''
        # save the modified date
        self.date_modified = timezone.now()

        # Save the modified_by field if a request is provided and the user is authenticated.
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            self.modified_by = request.user
        elif self.pk is not None and self.modified_by is None:
            self.modified_by = self

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.phone_number})"
