from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from services.documents import ServiceDocument


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
            'content',
            'cancelled',
            'photo',
            'created_at',
            'owner',
            'coordinates'
        )
