from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from activities.documents import (
    ActivityDocument,
    ActivityAttendanceDocument,
    ActivityAttendanceRequestDocument,
    ActivityRateDocument
)


class ActivityDocumentSerializer(DocumentSerializer):
    class Meta:
        document = ActivityDocument
        fields = (
            'uuid',
            'title',
            'description',
            'start_date',
            'duration',
            'repetition_term',
            'privacy_status',
            'participant_limit',
            'participant_picking',
            'category',
            'content',
            'cancelled',
            'photo',
            'created_at',
            'owner',
            'coordinates',
            'location',
            'formatted_address',
            'location_type_icon',
            'category_name',
        )


class ActivityAttendanceDocumentSerializer(DocumentSerializer):
    class Meta:
        document = ActivityAttendanceDocument
        fields = (
            'uuid',
            'member',
            'owner',
            'service',
            'status',
            'created_at',
        )


class ActivityAttendanceRequestDocumentSerializer(DocumentSerializer):
    class Meta:
        document = ActivityAttendanceRequestDocument
        fields = (
            'uuid',
            'member',
            'owner',
            'service',
            'status',
            'created_at',
        )


class ActivityRateDocumentSerializer(DocumentSerializer):
    class Meta:
        document = ActivityRateDocument
        fields = (
            'uuid',
            'voter',
            'service',
            'rate',
            'content',
            'created_at',
        )
