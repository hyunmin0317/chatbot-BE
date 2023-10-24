from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from api.models import Answer
from api.serializers import AnswerSerializer


@api_view(['POST'])
def find_answer(request):
    answer = get_object_or_404(Answer, input=request.data['question'])
    serializer = AnswerSerializer(answer)
    return Response(serializer.data, status=status.HTTP_200_OK)


class AnswerAPI(APIView):
    def get(self, request):
        answers = Answer.objects.all().order_by('-count')[:5]
        serializer = AnswerSerializer(answers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        for answer in Answer.objects.all():
            answer.count = 0
            answer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
