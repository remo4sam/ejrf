from questionnaire.models.base import BaseModel
from django.db import models


class QuestionGroupOrder(BaseModel):
    question = models.ForeignKey("Question", blank=False, null=False, related_name="orders")
    order = models.PositiveIntegerField(blank=False, null=False)
    question_group = models.ForeignKey("QuestionGroup", blank=False, null=True, related_name="orders")

    class Meta:
        ordering = ('order',)
        app_label = 'questionnaire'
        unique_together = ('order', 'question_group', 'question')

    def is_last_answer_type_in_group(self):
        return self.first_by('-order')

    def first_by(self, attribute_string):
        ordered_by_attributes = QuestionGroupOrder.objects.filter(question_group=self.question_group,
                                                                  question__answer_type=self.question.answer_type).\
            order_by(attribute_string)
        return self == ordered_by_attributes[0]

    def is_first_answer_type_in_group(self):
        return self.first_by('order')