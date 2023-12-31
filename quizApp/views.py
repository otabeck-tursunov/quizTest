import random

from django.db.models import Func
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import *


class Random(Func):
    function = 'RANDOM'


class Categories(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializerDefault


class Quizzes(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="category_id",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="filter by Category ID"
            ),
        ],

    )
    def get(self, request):
        category_id = request.query_params.get('category_id')
        quizzes = Quiz.objects.all()
        if category_id:
            if int(category_id) not in Category.objects.values_list('id', flat=True):
                return Response({"message": "Invalid Category ID"}, status=status.HTTP_400_BAD_REQUEST)
            quizzes = quizzes.filter(category__id=category_id)
        serializer = QuizzesSerializer(quizzes, many=True)

        if serializer:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "Quiz not found"}, status=status.HTTP_204_NO_CONTENT)


class RandomQuiz(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='category_id',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='filter by Category ID'
            ),
        ],
    )
    def get(self, reqeust):
        category_id = reqeust.query_params.get('category_id')
        quizzes = Quiz.objects.all()

        if category_id:
            if int(category_id) not in Category.objects.values_list('id', flat=True):
                return Response({"message": "Invalid category ID"}, status=status.HTTP_400_BAD_REQUEST)
            quizzes = quizzes.filter(category__id=category_id)

        randomQuiz = random.choice(quizzes)
        serializer = QuizzesSerializer(randomQuiz)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Questions(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="category_id",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="filter by Category ID"
            ),
            openapi.Parameter(
                name="quiz_id",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="filter by Quiz ID"
            ),
            openapi.Parameter(
                name="amount",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="amount of questions"
            ),
            openapi.Parameter(
                name="shuffle",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_BOOLEAN,
                description="shuffle the list"

            )
        ]
    )
    def get(self, request):
        category_id = request.query_params.get('category_id')
        quiz_id = request.query_params.get('quiz_id')
        amount = request.query_params.get('amount')
        shuffle = request.query_params.get('shuffle', False)

        questions = Question.objects.all()
        quizzes = Quiz.objects.all()

        if category_id:
            if int(category_id) not in Category.objects.values_list('id', flat=True):
                return Response({"message": "Invalid Category ID"}, status=status.HTTP_400_BAD_REQUEST)
            quizzes = quizzes.filter(category__id=category_id)

        if quiz_id:
            if int(quiz_id) not in quizzes.values_list('id', flat=True):
                return Response({"message": "Invalid Quiz ID"}, status=status.HTTP_400_BAD_REQUEST)
            quizzes = quizzes.filter(id=quiz_id)

        questions = questions.filter(quiz__id__in=quizzes.values_list('id', flat=True))

        if shuffle == 'true':
            questions = questions.order_by(Random())

        if amount:
            if int(amount) > len(questions):
                return Response({'message': 'Not enough multiple choice questions!'},
                                status=status.HTTP_411_LENGTH_REQUIRED)
            questions = questions[:int(amount)]

        serializer = QuestionsSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
            quizzes = quizzes.filter(category__id=category_id)
            questions = questions.filter(quiz__id__in=quizzes.values_list('id', flat=True))

        if quiz_id:
            if int(quiz_id) not in quizzes.values_list('id', flat=True) and quiz_id:
                return Response({'error': 'Invalid Quiz ID'}, status=status.HTTP_400_BAD_REQUEST)
            questions = questions.filter(quiz__id=quiz_id)

        if questions:
            random_question = random.choice(questions)
            serializer = QuestionSerializerDefault(random_question)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "Question not found"}, status=status.HTTP_204_NO_CONTENT)


class Answers(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='question_id',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='question ID'
            )
        ]
    )
    def get(self, request):
        question_id = request.query_params.get('question_id')
        answers = Answer.objects.all()

        if question_id:
            if int(question_id) not in answers.values_list('id', flat=True):
                return Response({'error': 'Invalid Question ID'}, status=status.HTTP_400_BAD_REQUEST)
            answers = answers.filter(question__id=question_id)

        serializer = AnswersSerializer(answers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
