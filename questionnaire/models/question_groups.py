from questionnaire.models.base import BaseModel
from django.db import models
from questionnaire.utils.model_utils import map_question_type_with


class QuestionGroup(BaseModel):
    question = models.ManyToManyField("Question", blank=False, null=False, related_name="question_group")
    subsection = models.ForeignKey("SubSection", blank=False, null=False, related_name="question_group")
    name = models.CharField(max_length=200, blank=False, null=True)
    instructions = models.TextField(blank=False, null=True)
    parent = models.ForeignKey("QuestionGroup", null=True, related_name="sub_group")
    order = models.PositiveIntegerField(null=True, blank=False)
    allow_multiples = models.BooleanField(default=False)
    grid = models.BooleanField(default=False)
    display_all = models.BooleanField(default=False)

    class Meta:
        ordering = ('order',)
        app_label = 'questionnaire'

    def all_questions(self):
        return self.question.all()

    def sub_groups(self):
        return self.sub_group.all()

    def and_sub_group_questions(self):
        questions = list(self.all_questions())
        for sub_group in self.sub_groups():
            questions.extend(sub_group.all_questions())
        return questions

    def ordered_questions(self):
        return [order.question for order in self.question_orders()]

    def question_orders(self):
        if self.parent:
            return self.parent.orders.order_by('order').filter(question__in=self.all_questions()).select_related()
        return self.orders.order_by('order').select_related()

    def has_at_least_two_questions(self):
        return self.question.count() > 1

    def primary_question(self):
        return self.question.filter(is_primary=True)

    def all_non_primary_questions(self):
        non_primary_questions = filter(lambda question: not question.is_primary, self.ordered_questions())
        return non_primary_questions

    def has_subgroups(self):
        return self.sub_group.exists()

    def max_questions_order(self):
        group_orders = self.orders.order_by('-order')
        if group_orders.exists():
            return group_orders[0].order
        return 0

    def map_orders_with_answer_type(self, mapped_orders):
        orders = self.orders.order_by('order').select_related()
        if self.primary_question() and self.grid:
            for option in self.primary_question()[0].options.all():
                map_question_type_with(orders, mapped_orders, option)
        else:
            map_question_type_with(orders, mapped_orders)