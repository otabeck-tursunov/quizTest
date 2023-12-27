from django.contrib import admin

from quizApp.models import *

admin.site.register([Category, Quiz])


class AnswerInline(admin.TabularInline):
    model = Answer
    fields = ('text', 'is_correct')


class QuestionAdmin(admin.ModelAdmin):
    model = Question
    inlines = [AnswerInline]


admin.site.register(Question, QuestionAdmin)
