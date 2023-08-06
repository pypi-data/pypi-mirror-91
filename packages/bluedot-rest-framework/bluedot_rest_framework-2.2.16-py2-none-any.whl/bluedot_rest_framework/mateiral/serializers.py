from bluedot_rest_framework.utils.serializers import CustomSerializer
from bluedot_rest_framework import import_string

Material = import_string('material.models')


class MaterialSerializer(CustomSerializer):
    class Meta:
        model = Material
        fields = '__all__'
