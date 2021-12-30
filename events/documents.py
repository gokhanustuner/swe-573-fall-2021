from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import Event


@registry.register_document
class EventDocument(Document):
    class Index:
        name = 'events'

        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 1,
        }

    class Django:
        model = Event

        fields = [
            'uuid',
            'title',
            # 'owner',
        ]
