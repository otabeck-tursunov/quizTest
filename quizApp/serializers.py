from rest_framework.serializers import ModelSerializer
from .models import *


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class QuizSerializer(ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Quiz
        fields = '__all__'


class QuestionSerializer(ModelSerializer):
    quiz = QuizSerializer(read_only=True)

    class Meta:
        model = Question
        fields = '__all__'


class QuestionSerializerDefault(ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class AnswerSerializer(ModelSerializer):
    question = QuestionSerializerDefault(read_only=True)

    class Meta:
        model = Answer
        fields = '__all__'
