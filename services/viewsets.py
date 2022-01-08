from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_GEO_DISTANCE,
    LOOKUP_FILTER_GEO_POLYGON,
    LOOKUP_FILTER_GEO_BOUNDING_BOX,
    SUGGESTER_COMPLETION,
)
from django_elasticsearch_dsl_drf.filter_backends import (
    DefaultOrderingFilterBackend,
    FacetedSearchFilterBackend,
    FilteringFilterBackend,
    GeoSpatialFilteringFilterBackend,
    GeoSpatialOrderingFilterBackend,
    NestedFilteringFilterBackend,
    OrderingFilterBackend,
    SearchFilterBackend,
    SuggesterFilterBackend,
)
from django_elasticsearch_dsl_drf.pagination import LimitOffsetPagination
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

from .documents import (
    ServiceDocument,
    ServiceAttendanceDocument,
    ServiceAttendanceRequestDocument,
    ServiceRateDocument
)
from .serializers import (
    ServiceDocumentSerializer,
    ServiceAttendanceDocumentSerializer,
    ServiceAttendanceRequestDocumentSerializer,
    ServiceRateDocumentSerializer
)


class ServiceDocumentViewSet(DocumentViewSet):
    document = ServiceDocument
    serializer_class = ServiceDocumentSerializer
    lookup_field = 'uuid'
    filter_backends = [
        FacetedSearchFilterBackend,
        FilteringFilterBackend,
        OrderingFilterBackend,
        SearchFilterBackend,
        GeoSpatialFilteringFilterBackend,
        GeoSpatialOrderingFilterBackend,
        # NestedFilteringFilterBackend,
        DefaultOrderingFilterBackend,
        SuggesterFilterBackend,
    ]
    pagination_class = LimitOffsetPagination
    # Define search fields
    search_fields = (
        'title',
        'category',
        'owner.full_name',
        'full_address',
        'category_name',
    )
    # Define filtering fields
    filter_fields = {
        # 'id': None,
        'uuid': 'uuid.raw',
        'title': 'title.raw',
        # 'title': 'city.name.raw',
    }
    # Nested filtering fields
    """
    nested_filter_fields = {
        'continent_country': {
            'field': 'continent.country.name.raw',
            'path': 'continent.country',
        },
        'continent_country_city': {
            'field': 'continent.country.city.name.raw',
            'path': 'continent.country.city',
        },
    }
    """
    # Define geo-spatial filtering fields
    geo_spatial_filter_fields = {
        'coordinates': {
            'lookups': [
                LOOKUP_FILTER_GEO_BOUNDING_BOX,
                LOOKUP_FILTER_GEO_DISTANCE,
                LOOKUP_FILTER_GEO_POLYGON,

            ],
        },
    }
    # Define ordering fields
    ordering_fields = {
        # 'id': None,
        'created_at': None,
        'start_date': None,
        # 'city': 'city.name.raw',
        # 'country': 'city.country.name.raw',
        # 'zip_code': None,
    }
    # Define ordering fields
    geo_spatial_ordering_fields = {
        'coordinates': None,
    }
    # Specify default ordering
    ordering = (
        'created_at',
        # 'title.raw',
        # 'city.name.raw',
    )
    # Suggester fields
    suggester_fields = {
        'title_suggest': {
            'field': 'title.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        },
        # 'city_suggest': {
        #     'field': 'city.name.suggest',
        #     'suggesters': [
        #         SUGGESTER_COMPLETION,
        #     ],
        # },
        # 'country_suggest': {
        #     'field': 'city.country.name.suggest',
        #     'suggesters': [
        #         SUGGESTER_COMPLETION,
        #     ],
        # }
    }

    # Facets

    faceted_search_fields = {
        'title': {
            'field': 'title.raw',
            'enabled': True,
        }
        # 'city': {
        #     'field': 'city.name.raw',
        #     'enabled': True,
        # },
        # 'country': {
        #     'field': 'city.country.name.raw',
        #     'enabled': True,
        # },
    }


class ServiceAttendanceDocumentViewSet(DocumentViewSet):
    document = ServiceAttendanceDocument
    serializer_class = ServiceAttendanceDocumentSerializer
    lookup_field = 'uuid'

    # Define filtering fields
    filter_fields = {
        # 'id': None,
        'member_id': 'member.id',
        'service_id': 'service.id',
        # 'title': 'city.name.raw',
    }

    ordering_fields = {
        'created_at': None,
    }


class ServiceAttendanceRequestDocumentViewSet(DocumentViewSet):
    document = ServiceAttendanceRequestDocument
    serializer_class = ServiceAttendanceRequestDocumentSerializer
    lookup_field = 'uuid'

    # Define filtering fields
    filter_fields = {
        # 'id': None,
        'member_id': 'member.id',
        'service_id': 'service.id',
        # 'title': 'city.name.raw',
    }

    ordering_fields = {
        'created_at': None,
    }


class ServiceRateDocumentViewSet(DocumentViewSet):
    document = ServiceRateDocument
    serializer_class = ServiceDocumentSerializer
    lookup_field = 'uuid'

    # Define filtering fields
    filter_fields = {
        # 'id': None,
        'voter_id': 'voter.id',
        'service_id': 'service.id',
        # 'title': 'city.name.raw',
    }

    ordering_fields = {
        'created_at': None,
    }
