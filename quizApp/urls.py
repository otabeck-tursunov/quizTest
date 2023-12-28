from django.urls import path

from .views import *

urlpatterns = [
    path('categories/', Categories.as_view()),
    path('categories/<int:category_id>/quizzes/', QuizzesByCategory.as_view()),
    path('categories/<int:category_id>/questions/', QuestionsByCategory.as_view()),
    path('quizzes/', Quizzes.as_view()),
    path('quizzes/<int:quiz_id>/questions/', QuestionsByQuiz.as_view()),
    path('questions/', Questions.as_view()),
    path('questions/random/', RandomQuestion.as_view()),
    path('questions/<int:question_id>/answers/', AnswersByQuestion.as_view())
]
