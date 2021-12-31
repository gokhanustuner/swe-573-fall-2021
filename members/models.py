import uuid

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models
from location_field.models.plain import PlainLocationField
from django.utils.translation import gettext_lazy as _

MEMBER_DEFAULT_CREDIT = 20


class MemberManager(BaseUserManager):
    def create_user(
            self,
            email: str,
            password: str = None,
            is_super: bool = False,
            first_name: str = None,
            last_name: str = None,
            personal_characteristics: str = None,
            bio: str = None,
            talents: str = None,
            phone: str = None,
    ):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name.capitalize() if not is_super else '',
            last_name=last_name.capitalize() if not is_super else '',
            phone=phone,
            personal_characteristics=personal_characteristics if not is_super else '',
            bio=bio if not is_super else '',
            talents=talents if not is_super else '',
            location=MemberLocation(
                'latitude'
            )
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            is_super=True,
        )
        user.is_admin = True
        user.save(using=self._db)

        return user


class Member(AbstractBaseUser):

    def __str__(self):
        return self.first_name + self.last_name

    uuid = models.UUIDField(
        verbose_name=_('Member ID'),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    first_name = models.CharField(verbose_name=_('Firstname'), max_length=500)
    last_name = models.CharField(verbose_name=_('Lastname'), max_length=500)
    email = models.EmailField(verbose_name=_('Email'), unique=True)
    password = models.EmailField(verbose_name=_('Email'))
    phone = models.CharField(verbose_name=_('Phone number'), max_length=500, null=True)
    personal_characteristics = models.TextField(verbose_name=_('Personal characteristics'))
    bio = models.TextField(verbose_name=_('Short bio'))
    talents = models.TextField(verbose_name=_('Talents'))
    credit = models.PositiveIntegerField(verbose_name=_('Total credits'), default=MEMBER_DEFAULT_CREDIT)
    location = PlainLocationField(based_fields=['city'], zoom=7)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MemberManager()
    USERNAME_FIELD = 'email'


class SocialDirectedGraph(models.Model):
    source = models.ForeignKey(
        'Member',
        on_delete=models.CASCADE,
        verbose_name=_('Member following'),
        related_name='source'
    )
    target = models.ForeignKey(
        'Member',
        on_delete=models.CASCADE,
        verbose_name=_('Member followed'),
        related_name='target'
    )
