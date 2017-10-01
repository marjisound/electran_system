from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils import timezone
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.conf import settings


class MyUserManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, student_no=None, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not first_name:
            raise ValueError('Users must provide their first name')
        if not last_name:
            raise ValueError('Users must provide their last name')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=self.normalize_email(email),
            student_no=student_no,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

USERNAME_REGEX = '^[a-zA-Z0-9._+-]*$'


class MyUser(AbstractBaseUser):
    username = models.CharField(max_length=120,
                                validators=[
                                    RegexValidator(
                                        regex=USERNAME_REGEX,
                                        message=('Username must be Alphanumeric or contain'
                                                 'any of the following characters: " . _ + - "'),
                                        code='invalid_username'
                                    )
                                ],
                                unique=True,
                                verbose_name='Username')

    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    student_no = models.PositiveIntegerField(
            null=True,
            blank=True,
            unique=True,
            verbose_name='Student Number',
            default=None
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    created = models.DateTimeField(editable=False, null=True)
    modified = models.DateTimeField(null=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(MyUser, self).save(*args, **kwargs)

    def get_full_name(self):
        # The user is identified by their email address
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.last_name

    def __str__(self):              # __unicode__ on Python 2
        return self.first_name + ' ' + self.last_name + '(' + self.username + ')'

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


from allauth.account.views import PasswordResetView

from django.conf import settings
from django.dispatch import receiver
from django.http import HttpRequest
from django.middleware.csrf import get_token
from django.contrib.sites.models import Site


@receiver(models.signals.post_save, sender=settings.AUTH_USER_MODEL)
def send_reset_password_email(sender, instance, created, **kwargs):

    if created:

        # First create a post request to pass to the view
        request = HttpRequest()
        request.method = 'POST'

        # add the absolute url to be be included in email
        site = Site.objects.get(id=settings.SITE_ID).domain
        request.META['HTTP_HOST'] = site

        # pass the post form data
        request.POST = {
            'email': instance.email,
            'csrfmiddlewaretoken': get_token(HttpRequest())
        }
        PasswordResetView.as_view()(request)