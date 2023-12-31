from rest_framework.serializers import ModelSerializer
from .models import *


class CategorySerializerDefault(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class QuizSerializerDefault(ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'


class QuizzesSerializer(ModelSerializer):
    category = CategorySerializerDefault()

    class Meta:
        model = Quiz
        fields = '__all__'


class QuestionSerializerDefault(ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class QuestionsSerializer(ModelSerializer):
    quiz = QuizSerializerDefault()

    class Meta:
        model = Question
        fields = '__all__'


class AnswersSerializer(ModelSerializer):
    question = QuestionSerializerDefault()

    class Meta:
        model = Answer
        fields = '__all__'
