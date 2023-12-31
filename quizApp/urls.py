from django.urls import path

from .views import *

urlpatterns = [
    path('categories/', Categories.as_view()),
    path('quizzes/', Quizzes.as_view()),
    path('quizzes/random/', RandomQuiz.as_view()),
    path('questions/', Questions.as_view()),
    path('questions/random/', RandomQuestion.as_view()),
    path('answers/', Answers.as_view()),
]
