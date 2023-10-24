from django.urls import path
from api import views

app_name = 'api'

urlpatterns = [
    path('find', views.find_answer, name='find_answer'),
    path('count', views.AnswerAPI.as_view(), name='count'),
]
