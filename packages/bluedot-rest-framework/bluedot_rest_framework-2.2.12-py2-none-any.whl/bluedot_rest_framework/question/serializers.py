from bluedot_rest_framework.utils.serializers import CustomSerializer
from .models import Question, QuestionUser


class QuestionSerializer(CustomSerializer):

    class Meta:
        model = Question
        fields = '__all__'


class QuestionUserSerializer(CustomSerializer):

    class Meta:
        model = QuestionUser
        fields = '__all__'
