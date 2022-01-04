from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models
from location_field.models.plain import PlainLocationField
from django.utils.translation import gettext_lazy as _

MEMBER_DEFAULT_CREDIT = 20


class MemberManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError('Users must have an email address')
        if not full_name:
            raise ValueError('Users must have a full name')
        if not password:
            raise ValueError('Users must have a password')
        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
        )
        user.staff = is_staff
        user.admin = is_admin
        user.active = is_active
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, full_name, password=None):
        user = self.create_user(
            email,
            full_name=full_name,
            password=password,
            is_staff=True,
        )
        return user

    def create_superuser(self, email, full_name, password=None):
        user = self.create_user(
            email,
            full_name=full_name,
            password=password,
            is_staff=True,
            is_admin=True,
        )
        return user


class Member(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255)
    password = models.EmailField(verbose_name=_('Email'))
    credit = models.PositiveIntegerField(default=MEMBER_DEFAULT_CREDIT, null=True, blank=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    objects = MemberManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']  # python manage.py createsuperuser

    def __str__(self):
        return self.full_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_active(self):
        return self.active

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin


class MemberProfile(models.Model):

    member = models.OneToOneField(
        'Member',
        on_delete=models.CASCADE
    )
    personal_characteristics = models.TextField(verbose_name=_('Personal characteristics'))
    bio = models.TextField(verbose_name=_('Short bio'))
    talents = models.TextField(verbose_name=_('Talents'))
    location = PlainLocationField(based_fields=['city'], zoom=7)


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
