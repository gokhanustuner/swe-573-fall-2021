"""A module containing enumeration objects for Event model"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class EventRepetitionTerm(models.IntegerChoices):
    """Repetition term options of an event"""
    ONE_TIME = 1, _('One-Time')
    WEEKLY = 2, _('Weekly')
    MONTHLY = 3, _('Monthly')
    YEARLY = 4, _('Yearly')

    @staticmethod
    def one_time():
        return EventRepetitionTerm.ONE_TIME

    @staticmethod
    def weekly():
        return EventRepetitionTerm.WEEKLY

    @staticmethod
    def monthly():
        return EventRepetitionTerm.MONTHLY

    @staticmethod
    def yearly():
        return EventRepetitionTerm.YEARLY


class EventPrivacyStatus(models.IntegerChoices):
    """Privacy status options of an event"""
    PUBLIC = 1, _('Public')
    PRIVATE = 2, _('Private')

    @staticmethod
    def public():
        return EventPrivacyStatus.PUBLIC

    @staticmethod
    def private():
        return EventPrivacyStatus.PRIVATE


class EventParticipantPicking(models.IntegerChoices):
    """Participant picking options of an event"""
    FREE = 1, _('Free')
    PICK_PARTICIPANTS = 2, _('Pick participants')

    @staticmethod
    def free():
        return EventParticipantPicking.FREE

    @staticmethod
    def pick():
        return EventParticipantPicking.PICK_PARTICIPANTS


class EventCancelled(models.IntegerChoices):
    """Cancellation options of an event"""
    NO = 0, _('No')
    YES = 1, _('Yes')

    @staticmethod
    def no():
        return EventCancelled.NO

    @staticmethod
    def yes():
        return EventCancelled.YES
