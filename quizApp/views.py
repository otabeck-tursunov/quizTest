import random

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import *


class Categories(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class Quizzes(ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class QuizzesByCategory(APIView):
    def get(self, request, category_id):
        serializer = QuizSerializer(Quiz.objects.filter(category__id=category_id), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Questions(ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuestionsByQuiz(APIView):
    def get(self, request, quiz_id):
        query_set = Question.objects.filter(quiz__id=quiz_id)
        serializer = QuestionSerializer(query_set, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class QuestionsByCategory(APIView):
    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        quizzes = Quiz.objects.filter(category=category).values_list('id', flat=True)
        questions = Question.objects.filter(quiz__id__in=quizzes)
        serializer = QuestionSerializer(questions, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class RandomQuestion(APIView):
    @swagger_auto_schema(
        manual_parameters=[

            openapi.Parameter(
                name='category_id',
                in_=openapi.IN_QUERY,
                description='by Category ID',
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name='quiz_id',
                in_=openapi.IN_QUERY,
                description='by Quiz ID',
                type=openapi.TYPE_INTEGER
            ),
        ],
    )
    def get(self, request):
        category_id = request.query_params.get('category_id')
        quiz_id = request.query_params.get('quiz_id')
        questions = Question.objects.all()
        quizzes = Quiz.objects.all()

        if category_id:
            if int(category_id) not in Category.objects.values_list('id', flat=True):
                return Response({'error': 'Invalid Category ID'}, status=status.HTTP_400_BAD_REQUEST)
            quizzes = quizzes.filter(category_id=category_id)
            questions = questions.filter(quiz__id__in=quizzes.values_list('id', flat=True))

        if quiz_id:
            if int(quiz_id) not in quizzes.values_list('id', flat=True) and quiz_id:
                return Response({'error': 'Invalid Quiz ID'}, status=status.HTTP_400_BAD_REQUEST)
            questions = questions.filter(quiz__id=quiz_id)

        if questions:
            random_question = random.choice(questions)
            serializer = QuestionSerializer(random_question)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Question not found"}, status=status.HTTP_204_NO_CONTENT)


# class RandomQuiz(APIView):
#     def get(self, request):


class AnswersByQuestion(APIView):
    def get(self, request, question_id):
        question = get_object_or_404(Question, id=question_id)
        answers = Answer.objects.filter(question=question)
        serializer = AnswerSerializer(answers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
