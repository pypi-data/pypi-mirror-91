from rest_framework.decorators import action
from rest_framework.response import Response
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet
from bluedot_rest_framework import import_string


Material = import_string('material.models')
MaterialSerializer = import_string('material.serializers')


class MaterialView(CustomModelViewSet):
    model_class = Material
    serializer_class = MaterialSerializer
    filterset_fields = {
        'materia_type': {
            'field_type': 'int',
            'lookup_expr': ''
        },
        'title': {
            'field_type': 'string',
            'lookup_expr': '__icontains'
        },
        'category_id': {
            'field_type': 'int',
            'lookup_expr': ''
        },
        'extend_category_id': {
            'field_type': 'int',
            'lookup_expr': '__in'
        },
    }
