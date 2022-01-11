import json

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django_elasticsearch_dsl_drf.wrappers import dict_to_obj

MEMBER_DEFAULT_CREDIT = 5


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
        primary_key=True,
        related_name='profile',
        on_delete=models.CASCADE
    )
    personal_characteristics = models.TextField(verbose_name=_('Personal characteristics'), null=True, blank=True)
    bio = models.TextField(verbose_name=_('Short bio'), null=True, blank=True)
    talents = models.TextField(verbose_name=_('Talents'), null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to='members/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('members.show', kwargs={'pk': self.member.pk})

    def get_latitude(self):
        if self.location is not None and self.location != '':
            payload = json.loads(str(self.location).replace("\\'", '"'))
            if payload != '' and payload is not None:
                return payload['geometry']['location']['lat']
            else:
                return 0.0
        else:
            return 0.0

    def get_longitude(self):
        if self.location is not None and self.location != '':
            payload = json.loads(str(self.location).replace("\\'", '"'))
            if payload != '' and payload is not None:
                return payload['geometry']['location']['lng']
            else:
                return 0.0
        else:
            return 0.0

    def get_formatted_address(self):
        if self.location is not None and self.location != '':
            payload = json.loads(str(self.location).replace("\\'", '"'))
            if payload != '' and payload is not None:
                return payload['formatted_address']
            else:
                return ''
        else:
            return ''

    def get_location_type_icon(self):
        if self.location is not None and self.location != '':
            payload = json.loads(str(self.location).replace("\\'", '"'))
            if payload != '' and payload is not None:
                return payload['icon']
            else:
                return ''
        else:
            return ''

    @property
    def coordinates_field_indexing(self):
        """Location for indexing.

        Used in Elasticsearch indexing/tests of `geo_distance` native filter.
        """
        return {
            'lat': self.get_latitude(),
            'lon': self.get_longitude(),
        }

    @property
    def formatted_address_field_indexing(self):
        return self.get_formatted_address()

    @property
    def location_type_icon_field_indexing(self):
        return self.get_location_type_icon()

    @property
    def member_indexing(self):
        wrapper = dict_to_obj({
            'id': self.member.pk,
            'full_name': self.member.full_name,
            'credit': self.member.credit,
        })

        return wrapper


@receiver(post_save, sender=Member)
def create_member_profile(sender, instance, created, **kwargs):
    if created:
        MemberProfile.objects.create(member=instance)
        instance.profile.save()


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
