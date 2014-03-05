from questionnaire.models import Answer
from questionnaire.models.base import BaseModel
from django.db import models


class AnswerGroup(BaseModel):
    answer = models.ManyToManyField(Answer, null=True, related_name="answergroup")
    grouped_question = models.ForeignKey("QuestionGroup", null=True, related_name="answer_groups")
    row = models.CharField(max_length=6)

    @classmethod
    def next_row(cls):
        answer_rows = filter(None, cls.objects.values_list('row', flat=True))
        return int(max(answer_rows)) + 1 if answer_rows else 0