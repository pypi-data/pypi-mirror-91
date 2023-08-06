from rest_framework.decorators import action
from django.db.models import Q
from rest_framework.response import Response
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet, AllView
from bluedot_rest_framework import import_string


Material = import_string('material.models')
Tags = import_string('material.tags.models')
Event = import_string('event.models')
Event = import_string('event.models')
EventSerializer = import_string('event.serializers')
MaterialSerializer = import_string('material.serializers')


class FrontendView:
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

    @action(detail=False, methods=['get'], url_path='search-index', url_name='search-index')
    def search_index(self, request, *args, **kwargs):
        title = request.query_params.get('title', '')
        tags_queryset = Tags.objects.filter(title__icontains=title)
        tags_id = [item.id for item in tags_queryset]
        queryset = self.model_class.objects.filter(
            Q(title__icontains=title) | Q(tags_id__in=[tags_id]))
        if queryset is None:
            return Response([])
        material_type_list = []
        for item in queryset:
            if item.material_type not in material_type_list:
                material_type_list.append(item.material_type)
        return Response(material_type_list)

    @action(detail=False, methods=['get'], url_path='front_list', url_name='front_list')
    def front_list(self, request, *args, **kwargs):
        material_id_list = []
        event_id_list = []
        title = request.query_params.get('title', None)
        queryset = self.filter_queryset(self.get_queryset())
        report = queryset.filter(material_type=2)[0:5]
        product = queryset.filter(material_type=3)[0:3]
        all_list = [report] + [product]
        queryset_list = [item for item in report]+[item for item in product]
        event = Event.objects.filter(title__contains=title)[0:2]
        for item in queryset_list:
            material_id_list.append(item.id)
        for item in event:
            event_id_list.append(item.id)

        exclude_queryset = queryset.exclude(id__in=material_id_list)
        exclude_event_queryset = Event.objects.exclude(id__in=event_id_list)

        material_data = [self.get_serializer(
            item, many=True).data for item in all_list]
        exclude_data = self.get_serializer(exclude_queryset, many=True).data
        event_data = EventSerializer(event, many=True).data
        exclude_event_data = EventSerializer(
            exclude_event_queryset, many=True).data
        last_data = material_data + event_data + exclude_data + exclude_event_data
        page = self.paginate_queryset(queryset)
        if page is not None:
            return self.get_paginated_response(last_data)
        return Response([])

    @action(detail=False, methods=['get'], url_path='ad', url_name='ad')
    def ad(self, request, *args, **kwargs):
        category_id = request.query_params.get('category_id', None)
        _type = request.query_params.get('_type', None)
        queryset = self.model_class.objects.all()
        ad_data = []
        for item in queryset:
            if item.recommend:
                ad_list = item.recommend['ad']
                if '_list' in ad_list:
                    for i in ad_list['_list']:
                        if i['_type'] == int(_type) and i['category_id'] == category_id:
                            ad_data.append([item])
        material_data = [self.get_serializer(
            item, many=True).data for item in ad_data]
        if material_data:
            return Response(material_data)
        return Response([])
