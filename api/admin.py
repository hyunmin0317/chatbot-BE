from django.contrib import admin
from api.models import Answer, Result


class AnswerAdmin(admin.ModelAdmin):
    search_fields = ['input', 'query']
    list_display = ['input', 'query', 'count']


class ResultAdmin(admin.ModelAdmin):
    search_fields = ['uid', 'question', 'answer__input']
    list_display = ['uid', 'question', 'answer', 'pred', 'result']


admin.site.register(Answer, AnswerAdmin)
admin.site.register(Result, ResultAdmin)
