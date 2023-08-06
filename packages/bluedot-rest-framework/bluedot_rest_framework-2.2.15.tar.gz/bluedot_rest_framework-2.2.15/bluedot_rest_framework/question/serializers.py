from bluedot_rest_framework.utils.serializers import CustomSerializer
from rest_framework.serializers import CharField, JSONField, IntegerField
from .models import Question, QuestionUser


class QuestionSerializer(CustomSerializer):
    qa_id = IntegerField(required=False)
    qa = JSONField(required=False)

    class Meta:
        model = Question
        fields = '__all__'


class QuestionUserSerializer(CustomSerializer):

    class Meta:
        model = QuestionUser
        fields = '__all__'
