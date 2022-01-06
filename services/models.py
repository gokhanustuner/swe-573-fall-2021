import uuid
import json

from django_mysql.models import Model as MySQLModel, DynamicField
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django_elasticsearch_dsl_drf.wrappers import dict_to_obj


class Service(models.Model):

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.title

    class ServiceRepetitionTerm(models.IntegerChoices):
        """Repetition term options of a service"""
        ONE_TIME = 1, _('One-Time')
        WEEKLY = 2, _('Weekly')
        MONTHLY = 3, _('Monthly')
        YEARLY = 4, _('Yearly')

    class ServicePrivacyStatus(models.IntegerChoices):
        """Privacy status options of a service"""
        PUBLIC = 1, _('Public')
        PRIVATE = 2, _('Private')

    class ServiceParticipantPicking(models.IntegerChoices):
        """Participant picking options of a service"""
        FREE = 1, _('Free')
        PICK_PARTICIPANTS = 2, _('Pick participants')

    class ServiceCancelled(models.IntegerChoices):
        """Cancellation options of a service"""
        NO = 0, _('No')
        YES = 1, _('Yes')

    class ServiceCategory(models.IntegerChoices):
        """Category options of a service"""
        FOOD = 1, _('Food')
        MUSIC = 2, _('Music')
        EDUCATION = 3, _('Education')
        ARTS = 4, _('Arts')
        ENTERTAINMENT = 5, _('Entertainment')
        TECHNICAL = 6, _('Technical')
        CRAFTSMANSHIP = 7, _('Craftsmanship')
        REPAIR_AND_MAINTENANCE = 8, _('Repair and maintenance')

    uuid = models.UUIDField(
        verbose_name=_('Service ID'),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    title = models.CharField(verbose_name=_('Title'), max_length=500)
    description = models.TextField(verbose_name=_('Service description'))
    location = models.TextField()
    owner = models.ForeignKey(
        'members.Member',
        on_delete=models.CASCADE,
        verbose_name=_('Service owner')
    )
    start_date = models.DateTimeField(verbose_name=_('Start date'))
    credit = models.PositiveIntegerField(verbose_name=_('Credit'))
    repetition_term = models.PositiveSmallIntegerField(
        verbose_name=_('Repetition term'),
        choices=ServiceRepetitionTerm.choices,
        default=ServiceRepetitionTerm.ONE_TIME,
    )
    privacy_status = models.PositiveSmallIntegerField(
        verbose_name=_('Privacy status'),
        choices=ServicePrivacyStatus.choices,
        default=ServicePrivacyStatus.PUBLIC,
    )
    participant_limit = models.PositiveIntegerField(verbose_name=_('Participant limit'), default=0)
    participant_picking = models.PositiveSmallIntegerField(
        verbose_name=_('Participant picking'),
        choices=ServiceParticipantPicking.choices,
        default=ServiceParticipantPicking.FREE,
    )
    category = models.PositiveSmallIntegerField(
        verbose_name=_('Service category'),
        choices=ServiceCategory.choices,
        default=ServiceCategory.FOOD,
    )
    content = models.TextField(verbose_name=_('Service content'))
    cancelled = models.BooleanField(
        verbose_name='Cancelled',
        max_length=1,
        choices=ServiceCancelled.choices,
        default=ServiceCancelled.NO,
    )
    photo = models.ImageField(upload_to='services', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def is_one_time_service(self):
        return self.repetition_term == self.ServiceRepetitionTerm.ONE_TIME

    def is_weekly_service(self):
        return self.repetition_term == self.ServiceRepetitionTerm.WEEKLY

    def is_monthly_service(self):
        return self.repetition_term == self.ServiceRepetitionTerm.MONTHLY

    def is_yearly_service(self):
        return self.repetition_term == self.ServiceRepetitionTerm.YEARLY

    def is_public(self):
        return self.privacy_status == self.ServicePrivacyStatus.PUBLIC

    def is_private(self):
        return self.privacy_status == self.ServicePrivacyStatus.PRIVATE

    def requires_participant_picking(self):
        return self.participant_picking == self.ServiceParticipantPicking.PICK_PARTICIPANTS

    def attendance_free(self):
        return self.participant_picking == self.ServiceParticipantPicking.FREE

    def is_cancelled(self):
        return self.cancelled == self.ServiceCancelled.YES

    def get_absolute_url(self):
        return reverse('services.detail', kwargs={'pk': self.pk})

    def get_latitude(self):
        payload = json.loads(str(self.location).replace("\\'", '"'))
        return payload['geometry']['location']['lat']

    def get_longitude(self):
        payload = json.loads(str(self.location).replace("\\'", '"'))
        return payload['geometry']['location']['lng']

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
    def owner_indexing(self):
        wrapper = dict_to_obj({
            'id': self.owner.id,
            'full_name': self.owner.full_name,
            'credit': self.owner.credit,
        })

        return wrapper


class ServiceAttendanceRequest(models.Model):

    class ServiceAttendanceRequestStatus(models.IntegerChoices):
        """Approval status options of a service request"""
        APPROVED = 1, _('Approved')
        DECLINED = 2, _('Declined')
        WAITING_FOR_APPROVAL = 3, _('Waiting for service owner\'s approval')

    uuid = models.UUIDField(
        verbose_name=_('Service attendance request ID'),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    member = models.OneToOneField(
        'members.Member',
        on_delete=models.CASCADE,
        verbose_name=_('Member requesting to attend to the service')
    )
    service = models.OneToOneField(
        'Service',
        on_delete=models.CASCADE,
        verbose_name=_('Service requested to attend')
    )
    status = models.PositiveSmallIntegerField(
        verbose_name=_('Service attendance request status'),
        choices=ServiceAttendanceRequestStatus.choices,
        default=ServiceAttendanceRequestStatus.WAITING_FOR_APPROVAL,
    )
    created_at = models.DateTimeField(auto_now_add=True)


class ServiceAttendance(models.Model):

    class ServiceAttendanceStatus(models.IntegerChoices):
        """Approval status options of a service request"""
        ACTIVE = 1, _('Active')
        CANCELLED = 2, _('Cancelled')

    uuid = models.UUIDField(
        verbose_name=_('Service attendance ID'),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    member = models.OneToOneField(
        'members.Member',
        on_delete=models.CASCADE,
        verbose_name=_('Member attending to the service')
    )

    service = models.OneToOneField(
        'Service',
        on_delete=models.CASCADE,
        verbose_name=_('Attended service')
    )
    status = models.PositiveSmallIntegerField(
        verbose_name=_('Service attendance status'),
        choices=ServiceAttendanceStatus.choices,
        default=ServiceAttendanceStatus.ACTIVE,
    )
    date = models.DateTimeField(verbose_name=_('Start date'))


class ServiceRate(models.Model):
    class ServiceRateValue(models.IntegerChoices):
        """Service rate values"""
        TERRIBLE = 1, _('Terrible')
        BAD = 2, _('Bad')
        NEUTRAL = 3, _('Neutral')
        GOOD = 4, _('Good')
        EXCELLENT = 5, _('Excellent')
    uuid = models.UUIDField(
        verbose_name=_('Service rate ID'),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    voter = models.OneToOneField(
        'members.Member',
        on_delete=models.CASCADE,
        verbose_name=_('Member attending to the service')
    )
    service = models.OneToOneField(
        'Service',
        on_delete=models.CASCADE,
        verbose_name=_('Attended service')
    )
    rate = models.PositiveSmallIntegerField(
        verbose_name=_('Service rate value'),
        choices=ServiceRateValue.choices,
    )
    content = models.TextField(verbose_name=_('Member comment for service'))
    created_at = models.DateTimeField(auto_now_add=True)
