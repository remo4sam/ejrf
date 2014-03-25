from questionnaire.models.base import BaseModel
from django.db import models


class QuestionGroupOrder(BaseModel):
    question = models.ForeignKey("Question", blank=False, null=False, related_name="orders")
    order = models.PositiveIntegerField(blank=False, null=False)
    question_group = models.ForeignKey("QuestionGroup", blank=False, null=True, related_name="orders")

    class Meta:
        ordering = ('order',)
        app_label = 'questionnaire'

    def is_last_answer_type_in_group(self):
        max_order_of_same_type = QuestionGroupOrder.objects.filter(question_group=self.question_group,
                                                                   question__answer_type=self.question.answer_type).\
                                                                    order_by('-order')
        return self == max_order_of_same_type[0]