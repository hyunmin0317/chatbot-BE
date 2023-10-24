from rest_framework import serializers

from api.models import Answer


class AnswerSerializer(serializers.ModelSerializer):
    output = serializers.JSONField()
    class Meta:
        model = Answer
        fields = '__all__'
