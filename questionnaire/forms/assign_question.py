from django.forms import Form
from django import forms
from questionnaire.models import Question


class AssignQuestionForm(Form):
    questions = forms.ModelMultipleChoiceField(queryset=None, label='')

    def __init__(self, *args, **kwargs):
        self.subsection = kwargs.pop('subsection', None)
        self.region = kwargs.pop('region', None)
        super(AssignQuestionForm, self).__init__(*args, **kwargs)
        self.fields['questions'].queryset = self._get_questions_query_set()

    def _get_questions_query_set(self):
        query_set = Question.objects.all()
        if self.region:
            return query_set.filter(region=self.region)
        return query_set

    def save(self, commit=True, *args, **kwargs):
        if self.subsection.question_group.count() > 1:
            question_group = self.subsection.question_group.order_by('-order')[0]
        else:
            question_group = self.subsection.question_group.get_or_create()[0]
        args = list(self.cleaned_data['questions'])
        question_group.question.add(*args)
        self._create_group_orders(question_group)

    def _create_group_orders(self, question_group):
        max_order = question_group.max_questions_order()
        for index, question in enumerate(self.cleaned_data['questions']):
            question.orders.create(question_group=question_group, order=max_order+index+1)
