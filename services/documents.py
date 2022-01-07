from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl_drf.compat import KeywordField, StringField
from elasticsearch_dsl import analyzer
from services.models import Service, ServiceAttendance, ServiceAttendanceRequest
from members.models import Member

# Name of the Elasticsearch index
SERVICE_INDEX = Index('services')
SERVICE_ATTENDANCE_INDEX = Index('service_attendance')
SERVICE_ATTENDANCE_REQUEST_INDEX = Index('service_attendance_requests')

SERVICE_INDEX.settings(
    number_of_shards=1,
    number_of_replicas=0,
)

SERVICE_ATTENDANCE_INDEX.settings(
    number_of_shards=1,
    number_of_replicas=0,
)

SERVICE_ATTENDANCE_REQUEST_INDEX.settings(
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
    """ServiceDocument Elasticsearch document."""

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
            'credit': fields.IntegerField()
        }
    )
    location = fields.TextField()
    # Formatted address
    formatted_address = StringField(
        attr='formatted_address_field_indexing',
        fields={
            'raw': KeywordField(),
            'suggest': fields.Completion(),
        }
    )
    location_type_icon = StringField(attr='location_type_icon_field_indexing')
    category_name = StringField(
        attr="category_name_field_indexing",
        fields={
            'raw': KeywordField(),
            'suggest': fields.Completion(),
        },
    )
    coordinates = fields.GeoPointField(attr='coordinates_field_indexing')

    class Django:
        """Meta options."""
        model = Service  # The model associate with this Document

        related_models = [Member]

    def get_queryset(self):
        return super().get_queryset().select_related(
            'owner'
        )

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Member):
            return related_instance.memberprofile.all()


@SERVICE_ATTENDANCE_INDEX.doc_type
class ServiceAttendanceDocument(Document):
    uuid = StringField(
        fields={
            'raw': KeywordField(),
        },
    )

    owner = fields.ObjectField(
        properties={
            'id': fields.IntegerField(),
            'full_name': StringField(),
            'credit': fields.IntegerField()
        }
    )

    member = fields.ObjectField(
        properties={
            'id': fields.IntegerField(),
            'full_name': StringField(),
            'credit': fields.IntegerField()
        }
    )

    service = fields.ObjectField(
        properties={
            'uuid': StringField(),
            'title': StringField(),
        }
    )

    status = fields.IntegerField()

    class Django:
        """Meta options."""
        model = ServiceAttendance  # The model associate with this Document

        related_models = [Member, Service]

    def get_member_queryset(self):
        return super().get_queryset().select_related(
            'member'
        )

    def get_service_queryset(self):
        return super().get_queryset().select_related(
            'service'
        )

    def get_owner_queryset(self):
        return super().get_queryset().select_related(
            'owner'
        )

    def get_instances_from_related(self, related_instance):
        pass


@SERVICE_ATTENDANCE_REQUEST_INDEX.doc_type
class ServiceAttendanceRequestDocument(Document):
    uuid = StringField(
        fields={
            'raw': KeywordField(),
        },
    )

    owner = fields.ObjectField(
        properties={
            'id': fields.IntegerField(),
            'full_name': StringField(),
            'credit': fields.IntegerField()
        }
    )

    member = fields.ObjectField(
        properties={
            'id': fields.IntegerField(),
            'full_name': StringField(),
            'credit': fields.IntegerField()
        }
    )

    service = fields.ObjectField(
        properties={
            'uuid': StringField(),
            'title': StringField(),
        }
    )

    status = fields.IntegerField()
    created_at = fields.DateField()

    class Django:
        """Meta options."""
        model = ServiceAttendanceRequest  # The model associate with this Document

        related_models = [Member, Service]

    def get_instances_from_related(self, related_instance):
        pass
