from django.db import models



class Category(models.Model):
    name = models.CharField(max_length=255)


class Quiz(models.Model):
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name='quizzes')
    title = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'quizzes'


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.DO_NOTHING, related_name='questions')
    date_updated = models.DateTimeField(auto_now=True)

    SCALE = (
        (0, 'fundamental'),
        (1, 'beginner'),
        (2, 'intermediate'),
        (3, 'advanced'),
        (4, 'expert')
    )
    # technique = models.IntegerField()
    text = models.CharField(max_length=255)
    difficulty = models.IntegerField(choices=SCALE, default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING, related_name='answers')
    text = models.CharField(max_length=255)
    date_updated = models.DateTimeField(auto_now=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text