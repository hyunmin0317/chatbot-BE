from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from api.apps import ApiConfig
from api.chatbot.inference import koelectra_chatbot
from api.models import Answer, Result
from api.serializers import AnswerSerializer


@api_view(['POST'])
def search_answer(request):
    threshold = 0.5
    uid, question = request.data['uid'], request.data['question']
    answer, pred = koelectra_chatbot(uid, question, ApiConfig.model, ApiConfig.tokenizer, ApiConfig.device, dataset=Answer.objects.all())
    result, stat = False, status.HTTP_204_NO_CONTENT
    if pred > threshold:
        answer.count += 1
        answer.save()
        result, stat = True, status.HTTP_200_OK
    Result.objects.create(uid=uid, question=question, answer=answer, pred=pred, result=result)
    serializer = AnswerSerializer(answer)
    return Response(serializer.data, status=stat)


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
