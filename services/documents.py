from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl_drf.compat import KeywordField, StringField
from elasticsearch_dsl import analyzer
from services.models import Service
from members.models import Member

# Name of the Elasticsearch index
SERVICE_INDEX = Index('services')

SERVICE_INDEX.settings(
    number_of_shards=1,
    number_of_replicas=0,
)

html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)


@SERVICE_INDEX.doc_type
class ServiceDocument(Document):
    """Publisher Elasticsearch document."""

    uuid = StringField(
        fields={
            'raw': KeywordField(),
        },
    )

    title = StringField(
        attr='title',
        fields={
            'raw': KeywordField(),
            'suggest': fields.Completion(),
        },
    )
    description = fields.TextField()
    start_date = fields.DateField()
    credit = fields.IntegerField()
    repetition_term = StringField(
        analyzer=html_strip,
        fields={
            'raw': KeywordField(),
        }
    )
    privacy_status = StringField(
        analyzer=html_strip,
        fields={
            'raw': KeywordField(),
        }
    )
    participant_limit = fields.IntegerField()
    participant_picking = StringField(
        analyzer=html_strip,
        fields={
            'raw': KeywordField(),
        }
    )
    category = StringField(
        analyzer=html_strip,
        fields={
            'raw': KeywordField(),
        }
    )
    content = fields.TextField()
    cancelled = StringField(
        analyzer=html_strip,
        fields={
            'raw': KeywordField(),
        }
    )
    photo = fields.FileField()
    created_at = fields.DateField()

    owner = fields.ObjectField(
        properties={
            'id': fields.IntegerField(),
            'full_name': StringField(
                fields={
                    'raw': KeywordField(),
                    'suggest': fields.Completion(),
                }
            ),
            'full_name': fields.TextField(),
            'credit': fields.IntegerField()
        }
    )
    location = fields.TextField()
    # Formatted address
    formatted_address = StringField(
        attr='formatted_address_field_indexing',
        fields={
            'raw': KeywordField(),
        }
    )
    location_type_icon = StringField(attr='location_type_icon_field_indexing')
    coordinates = fields.GeoPointField(attr='coordinates_field_indexing')

    class Django:
        """Meta options."""
        model = Service  # The model associate with this Document

        related_models = [Member]

    def get_queryset(self):
        return super().get_queryset().select_related(
            'owner'
        )

    """
    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Member):
            return related_instance.memberprofile.all()
    """
