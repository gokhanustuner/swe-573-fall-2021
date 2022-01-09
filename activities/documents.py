from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl_drf.compat import KeywordField, StringField
from elasticsearch_dsl import analyzer
from activities.models import Activity, ActivityAttendance, ActivityAttendanceRequest, ActivityRate
from members.models import Member

# Name of the Elasticsearch index
ACTIVITY_INDEX = Index('activities')
ACTIVITY_ATTENDANCE_INDEX = Index('activity_attendance')
ACTIVITY_ATTENDANCE_REQUEST_INDEX = Index('activity_attendance_requests')
ACTIVITY_RATE_INDEX = Index('activity_rates')

ACTIVITY_INDEX.settings(
    number_of_shards=1,
    number_of_replicas=0,
)

ACTIVITY_ATTENDANCE_INDEX.settings(
    number_of_shards=1,
    number_of_replicas=0,
)

ACTIVITY_ATTENDANCE_REQUEST_INDEX.settings(
    number_of_shards=1,
    number_of_replicas=0,
)

ACTIVITY_RATE_INDEX.settings(
    number_of_shards=1,
    number_of_replicas=0,
)

html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)


@ACTIVITY_INDEX.doc_type
class ActivityDocument(Document):
    """ActivityDocument Elasticsearch document."""

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
    duration = fields.IntegerField()
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
    delivered = StringField(
        analyzer=html_strip,
        fields={
            'raw': KeywordField(),
        }
    )
    photo = fields.FileField()
    created_at = fields.DateField()

    owner = fields.NestedField(
        properties={
            'id': fields.IntegerField(),
            'full_name': StringField(
                fields={
                    'raw': KeywordField(),
                    'suggest': fields.Completion(),
                }
            ),
            'credit': fields.IntegerField()
        }, include_in_root=True
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
        model = Activity  # The model associate with this Document

        related_models = [Member]

    def get_queryset(self):
        return super().get_queryset().select_related(
            'owner'
        )

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Member):
            return related_instance.memberprofile.all()


@ACTIVITY_ATTENDANCE_INDEX.doc_type
class ActivityAttendanceDocument(Document):
    uuid = StringField(
        fields={
            'raw': KeywordField(),
        },
    )

    owner = fields.NestedField(
        properties={
            'id': fields.IntegerField(),
            'full_name': StringField(),
            'credit': fields.IntegerField()
        }, include_in_root=True
    )

    member = fields.NestedField(
        properties={
            'id': fields.IntegerField(),
            'full_name': StringField(),
            'credit': fields.IntegerField()
        }, include_in_root=True
    )

    activity = fields.NestedField(
        properties={
            'uuid': StringField(),
            'title': StringField(),
        }, include_in_root=True
    )

    status = fields.IntegerField()
    created_at = fields.DateField()

    class Django:
        """Meta options."""
        model = ActivityAttendance  # The model associate with this Document

        related_models = [Member, Activity]

    def get_member_queryset(self):
        return super().get_queryset().select_related(
            'member'
        )

    def get_activity_queryset(self):
        return super().get_queryset().select_related(
            'activity'
        )

    def get_owner_queryset(self):
        return super().get_queryset().select_related(
            'owner'
        )

    def get_instances_from_related(self, related_instance):
        pass


@ACTIVITY_ATTENDANCE_REQUEST_INDEX.doc_type
class ActivityAttendanceRequestDocument(Document):
    uuid = StringField(
        fields={
            'raw': KeywordField(),
        },
    )

    owner = fields.NestedField(
        properties={
            'id': fields.IntegerField(),
            'full_name': StringField(),
            'credit': fields.IntegerField()
        }, include_in_root=True
    )

    member = fields.NestedField(
        properties={
            'id': fields.IntegerField(),
            'full_name': StringField(),
            'credit': fields.IntegerField()
        }, include_in_root=True
    )

    activity = fields.NestedField(
        properties={
            'uuid': StringField(),
            'title': StringField(),
        }, include_in_root=True
    )

    status = fields.IntegerField()
    created_at = fields.DateField()

    class Django:
        """Meta options."""
        model = ActivityAttendanceRequest  # The model associate with this Document

        related_models = [Member, Activity]

    def get_instances_from_related(self, related_instance):
        pass


@ACTIVITY_RATE_INDEX.doc_type
class ActivityRateDocument(Document):
    uuid = StringField(
        fields={
            'raw': KeywordField(),
        },
    )

    voter = fields.NestedField(
        properties={
            'id': fields.IntegerField(),
            'full_name': StringField(),
            'credit': fields.IntegerField()
        }, include_in_root=True
    )

    activity = fields.NestedField(
        properties={
            'uuid': StringField(),
            'title': StringField(),
        }, include_in_root=True
    )

    rate = fields.IntegerField()
    content = fields.TextField()
    created_at = fields.DateField()

    class Django:
        """Meta options."""
        model = ActivityRate  # The model associate with this Document

        related_models = [Member, Activity]

    def get_instances_from_related(self, related_instance):
        pass
