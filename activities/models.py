import uuid
import json

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_elasticsearch_dsl_drf.wrappers import dict_to_obj
from django.urls import reverse


class Activity(models.Model):
    CATEGORY_CHOICES = (1, _('Food')), (2, _('Music')), (3, _('Education')), (4, _('Arts')), (9, _('Sports')), \
                       (5, _('Entertainment')), (6, _('Technical')), (7, _('Craftsmanship')), \
                       (8, _('Repair and maintenance')), (10, _('Travel Activities'))

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.title

    class ActivityRepetitionTerm(models.IntegerChoices):
        """Repetition term options of an event"""
        ONE_TIME = 1, _('One-Time')
        WEEKLY = 2, _('Weekly')
        MONTHLY = 3, _('Monthly')
        YEARLY = 4, _('Yearly')

    class ActivityPrivacyStatus(models.IntegerChoices):
        """Privacy status options of an event"""
        PUBLIC = 1, _('Public')
        PRIVATE = 2, _('Private')

    class ActivityParticipantPicking(models.IntegerChoices):
        """Participant picking options of an event"""
        FREE = 1, _('Free')
        PICK_PARTICIPANTS = 2, _('Pick participants')

    class ActivityCancelled(models.IntegerChoices):
        """Cancellation options of an event"""
        NO = 0, _('No')
        YES = 1, _('Yes')

    class ActivityDelivered(models.IntegerChoices):
        """Delivery options of a service"""
        NO = 0, _('No')
        YES = 1, _('Yes')

    class ActivityCategory(models.IntegerChoices):
        """Category options of an event"""
        FOOD = 1, _('Food')
        MUSIC = 2, _('Music')
        EDUCATION = 3, _('Education')
        ARTS = 4, _('Arts')
        ENTERTAINMENT = 5, _('Entertainment')
        TECHNICAL = 6, _('Technical')
        CRAFTSMANSHIP = 7, _('Craftsmanship')
        REPAIR_AND_MAINTENANCE = 8, _('Repair and maintenance'),
        SPORTS = 9, _('Sports')
        TRAVEL_ACTIVITIES = (10, _('Travel Activities'))

    uuid = models.UUIDField(
        verbose_name=_('Event ID'),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    title = models.CharField(verbose_name=_('Title'), max_length=500)
    description = models.TextField(verbose_name=_('Description'))
    location = models.TextField()
    owner = models.ForeignKey(
        'members.Member',
        on_delete=models.CASCADE,
        verbose_name=_('Event owner')
    )
    start_date = models.DateTimeField(verbose_name=_('Start data'))
    duration = models.PositiveIntegerField(verbose_name=_('Duration'))
    repetition_term = models.PositiveSmallIntegerField(
        verbose_name=_('Repetition term'),
        choices=ActivityRepetitionTerm.choices,
        default=ActivityRepetitionTerm.ONE_TIME,
    )
    privacy_status = models.PositiveSmallIntegerField(
        verbose_name=_('Privacy status'),
        choices=ActivityPrivacyStatus.choices,
        default=ActivityPrivacyStatus.PUBLIC,
    )
    participant_limit = models.PositiveIntegerField(verbose_name=_('Participant limit'), default=0)
    participant_picking = models.PositiveSmallIntegerField(
        verbose_name='Participant picking',
        choices=ActivityParticipantPicking.choices,
        default=ActivityParticipantPicking.FREE,
    )
    category = models.PositiveSmallIntegerField(
        verbose_name=_('Event category'),
        choices=ActivityCategory.choices,
        default=ActivityCategory.FOOD,
    )
    content = models.TextField(verbose_name=_('Service content'))
    cancelled = models.BooleanField(
        verbose_name='Cancelled',
        max_length=1,
        choices=ActivityCancelled.choices,
        default=ActivityCancelled.NO,
    )

    delivered = models.BooleanField(
        verbose_name='Delivered',
        max_length=1,
        choices=ActivityDelivered.choices,
        default=ActivityDelivered.NO,
    )

    photo = models.ImageField(upload_to='activities', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def is_one_time_event(self):
        return self.repetition_term == self.ActivityRepetitionTerm.ONE_TIME

    def is_weekly_event(self):
        return self.repetition_term == self.ActivityRepetitionTerm.WEEKLY

    def is_monthly_event(self):
        return self.repetition_term == self.ActivityRepetitionTerm.MONTHLY

    def is_yearly_event(self):
        return self.repetition_term == self.ActivityRepetitionTerm.YEARLY

    def is_public(self):
        return self.privacy_status == self.ActivityRepetitionTerm.PUBLIC

    def is_private(self):
        return self.privacy_status == self.ActivityPrivacyStatus.PRIVATE

    def requires_participant_picking(self):
        return self.participant_picking == self.ActivityParticipantPicking.PICK_PARTICIPANTS

    def attendance_free(self):
        return self.participant_picking == self.ActivityParticipantPicking.FREE

    def is_cancelled(self):
        return self.cancelled == self.ActivityCancelled.YES

    def get_absolute_url(self):
        return reverse('activities.detail', kwargs={'pk': self.pk})

    def get_latitude(self):
        payload = json.loads(str(self.location).replace("\\'", '"'))
        return payload['geometry']['location']['lat']

    def get_longitude(self):
        payload = json.loads(str(self.location).replace("\\'", '"'))
        return payload['geometry']['location']['lng']

    def get_formatted_address(self):
        payload = json.loads(str(self.location).replace("\\'", '"'))
        return payload['formatted_address']

    def get_location_type_icon(self):
        payload = json.loads(str(self.location).replace("\\'", '"'))
        return payload['icon']

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
    def category_name_field_indexing(self):
        return list(filter(lambda x: x[0] == self.category, self.CATEGORY_CHOICES))[0][1]

    @property
    def owner_indexing(self):
        wrapper = dict_to_obj({
            'id': self.owner.pk,
            'full_name': self.owner.full_name,
            'credit': self.owner.credit,
        })

        return wrapper


class ActivityAttendanceRequest(models.Model):

    class Meta:
        ordering = ['created_at']

    class ActivityAttendanceRequestStatus(models.IntegerChoices):
        """Approval status options of an event request"""
        APPROVED = 1, _('Approved')
        DECLINED = 2, _('Declined')
        WAITING_FOR_APPROVAL = 3, _('Waiting for event owner\'s approval')

    uuid = models.UUIDField(
        verbose_name=_('Event attendance request ID'),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    member = models.ForeignKey(
        'members.Member',
        on_delete=models.CASCADE,
        verbose_name=_('Member requesting to attend to the event'),
        related_name='activity_member_requested'
    )
    activity = models.ForeignKey(
        'Activity',
        on_delete=models.CASCADE,
    )
    owner = models.ForeignKey(
        'members.Member',
        on_delete=models.CASCADE,
        verbose_name=_('Member to approve'),
        related_name='activity_owner',
        default=None
    )
    status = models.PositiveSmallIntegerField(
        verbose_name=_('Event attendance request status'),
        choices=ActivityAttendanceRequestStatus.choices,
        default=ActivityAttendanceRequestStatus.WAITING_FOR_APPROVAL,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def owner_indexing(self):
        wrapper = dict_to_obj({
            'id': self.owner.pk,
            'full_name': self.owner.full_name,
            'credit': self.owner.credit,
        })

        return wrapper

    @property
    def member_indexing(self):
        wrapper = dict_to_obj({
            'id': self.member.pk,
            'full_name': self.member.full_name,
            'credit': self.member.credit,
        })

        return wrapper

    @property
    def activity_indexing(self):
        wrapper = dict_to_obj({
            'uuid': self.activity.pk,
            'title': self.activity.title,
        })

        return wrapper


class ActivityAttendance(models.Model):

    class ActivityAttendanceStatus(models.IntegerChoices):
        """Attendance status options of an event"""
        ACTIVE = 1, _('Active')
        CANCELLED = 2, _('Cancelled')

    uuid = models.UUIDField(
        verbose_name=_('Event attendance ID'),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    member = models.ForeignKey(
        'members.Member',
        on_delete=models.CASCADE,
        verbose_name=_('Member attending to the event'),
        related_name='activity_member_attending'
    )

    activity = models.ForeignKey(
        'Activity',
        on_delete=models.CASCADE,
        verbose_name=_('Attended activity'),
        related_name='attendances',
    )

    owner = models.ForeignKey(
        'members.Member',
        on_delete=models.CASCADE,
        verbose_name=_('Member to approve'),
        related_name='activity_attendance_owner',
        default=None
    )

    status = models.PositiveSmallIntegerField(
        verbose_name=_('Activity attendance status'),
        choices=ActivityAttendanceStatus.choices,
        default=ActivityAttendanceStatus.ACTIVE,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def owner_indexing(self):
        wrapper = dict_to_obj({
            'id': self.owner.pk,
            'full_name': self.owner.full_name,
            'credit': self.owner.credit,
        })

        return wrapper

    @property
    def member_indexing(self):
        wrapper = dict_to_obj({
            'id': self.member.pk,
            'full_name': self.member.full_name,
            'credit': self.member.credit,
        })

        return wrapper

    @property
    def activity_indexing(self):
        wrapper = dict_to_obj({
            'uuid': self.activity.pk,
            'title': self.activity.title,
        })

        return wrapper


class ActivityRate(models.Model):

    class ActivityRateValue(models.IntegerChoices):
        """Event rate values"""
        TERRIBLE = 1, _('Terrible')
        BAD = 2, _('Bad')
        NEUTRAL = 3, _('Neutral')
        GOOD = 4, _('Good')
        EXCELLENT = 5, _('Excellent')
    uuid = models.UUIDField(
        verbose_name=_('Event rate ID'),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    voter = models.OneToOneField(
        'members.Member',
        on_delete=models.CASCADE,
        verbose_name=_('Member attending to the event')
    )
    activity = models.ForeignKey(
        'Activity',
        on_delete=models.CASCADE,
    )
    rate = models.PositiveSmallIntegerField(
        verbose_name=_('Event rate value'),
        choices=ActivityRateValue.choices,
    )
    content = models.TextField(verbose_name=_('Member comment for event'))
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def negative_rate_field_indexing(self):
        return 5 - self.rate

    @property
    def voter_indexing(self):
        wrapper = dict_to_obj({
            'id': self.voter.pk,
            'full_name': self.voter.full_name,
            'credit': self.voter.credit,
        })

        return wrapper

    @property
    def activity_indexing(self):
        wrapper = dict_to_obj({
            'uuid': self.activity.pk,
            'title': self.activity.title,
        })

        return wrapper
