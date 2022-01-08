from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from services.documents import ServiceDocument, ServiceAttendanceDocument, ServiceAttendanceRequestDocument


class ServiceDocumentSerializer(DocumentSerializer):
    class Meta:
        document = ServiceDocument
        fields = (
            'uuid',
            'title',
            'description',
            'start_date',
            'credit',
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
            'coordinates',
            'formatted_address',
            'location_type_icon',
            'category_name',
        )


class ServiceAttendanceDocumentSerializer(DocumentSerializer):
    class Meta:
        document = ServiceAttendanceDocument
        fields = (
            'uuid',
            'member',
            'owner',
            'service',
            'status',
            'created_at',
        )


class ServiceAttendanceRequestDocumentSerializer(DocumentSerializer):
    class Meta:
        document = ServiceAttendanceRequestDocument
        fields = (
            'uuid',
            'member',
            'owner',
            'service',
            'status',
            'created_at',
        )
