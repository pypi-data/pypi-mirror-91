from rest_framework.decorators import action
from rest_framework.response import Response
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet, AllView
from bluedot_rest_framework import import_string


Material = import_string('material.models')
Event = import_string('event.models')
EventSerializer = import_string('event.serializers')
MaterialSerializer = import_string('material.serializers')


class MaterialView(CustomModelViewSet, AllView):
    model_class = Material
    serializer_class = MaterialSerializer
    filterset_fields = {
        'material_type': {
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
        '_type': {
            'field_type': 'int',
            'lookup_expr': ''
        },
    }

    @action(detail=False, methods=['get'], url_path='event', url_name='event')
    def event(self, request, *args, **kwargs):
        material_type = request.query_params.get('material_type', None)
        if material_type == '5':
            queryset = Event.objects.all()
            serializer = EventSerializer(queryset, many=True)
        else:
            queryset = self.filter_queryset(self. get_queryset())
            serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
