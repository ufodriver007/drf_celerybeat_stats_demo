from rest_framework.serializers import ModelSerializer
from main.models import ParserCall


class ParserCallSerializer(ModelSerializer):
    class Meta:
        model = ParserCall
        fields = '__all__'
