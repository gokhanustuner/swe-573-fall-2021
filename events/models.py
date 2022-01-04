import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from location_field.models.plain import PlainLocationField


class Event(models.Model):

    def __str__(self):
        return self.title

    class EventRepetitionTerm(models.IntegerChoices):
        """Repetition term options of an event"""
        ONE_TIME = 1, _('One-Time')
        WEEKLY = 2, _('Weekly')
        MONTHLY = 3, _('Monthly')
        YEARLY = 4, _('Yearly')

    class EventPrivacyStatus(models.IntegerChoices):
        """Privacy status options of an event"""
        PUBLIC = 1, _('Public')
        PRIVATE = 2, _('Private')

    class EventParticipantPicking(models.IntegerChoices):
        """Participant picking options of an event"""
        FREE = 1, _('Free')
        PICK_PARTICIPANTS = 2, _('Pick participants')

    class EventCancelled(models.IntegerChoices):
        """Cancellation options of an event"""
        NO = 0, _('No')
        YES = 1, _('Yes')

    uuid = models.UUIDField(
        verbose_name=_('Event ID'),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    title = models.CharField(verbose_name=_('Title'), max_length=500)
    description = models.TextField(verbose_name=_('Description'))
    location = PlainLocationField(based_fields=['city'], zoom=7)
    owner = models.OneToOneField(
        'members.Member',
        on_delete=models.CASCADE,
        verbose_name=_('Event owner')
    )
    start_date = models.DateTimeField(verbose_name=_('Start data'))
    end_date = models.DateTimeField(verbose_name=_('End date'))
    repetition_term = models.PositiveSmallIntegerField(
        verbose_name=_('Repetition term'),
        choices=EventRepetitionTerm.choices,
        default=EventRepetitionTerm.ONE_TIME,
    )
    privacy_status = models.PositiveSmallIntegerField(
        verbose_name=_('Privacy status'),
        choices=EventPrivacyStatus.choices,
        default=EventPrivacyStatus.PUBLIC,
    )
    participant_limit = models.PositiveIntegerField(verbose_name=_('Participant limit'), default=0)
    participant_picking = models.PositiveSmallIntegerField(
        verbose_name='Participant picking',
        choices=EventParticipantPicking.choices,
        default=EventParticipantPicking.FREE,
    )
    cancelled = models.BooleanField(
        verbose_name='Cancelled',
        max_length=1,
        choices=EventCancelled.choices,
        default=EventCancelled.NO,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def is_one_time_event(self):
        return self.repetition_term == self.EventRepetitionTerm.ONE_TIME

    def is_weekly_event(self):
        return self.repetition_term == self.EventRepetitionTerm.WEEKLY

    def is_monthly_event(self):
        return self.repetition_term == self.EventRepetitionTerm.MONTHLY

    def is_yearly_event(self):
        return self.repetition_term == self.EventRepetitionTerm.YEARLY

    def is_public(self):
        return self.privacy_status == self.EventPrivacyStatus.PUBLIC

    def is_private(self):
        return self.privacy_status == self.EventPrivacyStatus.PRIVATE

    def requires_participant_picking(self):
        return self.participant_picking == self.EventParticipantPicking.PICK_PARTICIPANTS

    def attendance_free(self):
        return self.participant_picking == self.EventParticipantPicking.FREE

    def is_cancelled(self):
        return self.cancelled == self.EventCancelled.YES


class EventAttendanceRequest(models.Model):

    class EventAttendanceRequestStatus(models.IntegerChoices):
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
    member = models.OneToOneField(
        'members.Member',
        on_delete=models.CASCADE,
        verbose_name=_('Member requesting to attend to the event')
    )
    event = models.OneToOneField(
        'Event',
        on_delete=models.CASCADE,
        verbose_name=_('Event requested to attend')
    )
    status = models.PositiveSmallIntegerField(
        verbose_name=_('Event attendance request status'),
        choices=EventAttendanceRequestStatus.choices,
        default=EventAttendanceRequestStatus.WAITING_FOR_APPROVAL,
    )
    created_at = models.DateTimeField(auto_now_add=True)


class EventRate(models.Model):

    class EventRateValue(models.IntegerChoices):
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
    event = models.OneToOneField(
        'Event',
        on_delete=models.CASCADE,
        verbose_name=_('Attended event')
    )
    rate = models.PositiveSmallIntegerField(
        verbose_name=_('Event rate value'),
        choices=EventRateValue.choices,
    )
    content = models.TextField(verbose_name=_('Member comment for event'))
    created_at = models.DateTimeField(auto_now_add=True)
