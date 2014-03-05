from django.forms.formsets import formset_factory
from questionnaire.forms.answers import NumericalAnswerForm, TextAnswerForm, DateAnswerForm, MultiChoiceAnswerForm
from questionnaire.models import Question, AnswerGroup


ANSWER_FORM = {
    'Number': NumericalAnswerForm,
    'Text': TextAnswerForm,
    'Date': DateAnswerForm,
    'MultiChoice': MultiChoiceAnswerForm
}


class QuestionnaireEntryFormService(object):

    def __init__(self, section, initial={}, data=None, highlight=False):
        self.initial = initial
        self.data = data
        self.section = section
        self.question_orders = section.question_orders()
        self.formsets = self._formsets()
        self.ANSWER_FORM_COUNTER = self._initialize_form_counter()
        self._highlight_required_answers(highlight)
        self.form_answer_map = {}

    def next_ordered_form(self, question):
        next_question_type_count = self.ANSWER_FORM_COUNTER[question.answer_type]
        self.ANSWER_FORM_COUNTER[question.answer_type] += 1
        formset = self.formsets[question.answer_type][next_question_type_count]
        if question.is_primary and question.group().grid:
            formset.initial['response'] = question.get_option_at(self.ANSWER_FORM_COUNTER[question.answer_type])
        return formset

    @staticmethod
    def _initialize_form_counter():
        return {key: 0 for key in ANSWER_FORM.keys()}

    def _formsets(self):
        formsets = {}
        for answer_type in ANSWER_FORM.keys():
            orders = filter(lambda order: order.question.answer_type == answer_type, self.question_orders)
            if orders:
                _formset_factory = formset_factory(ANSWER_FORM[answer_type], max_num=len(orders))
                initial = self._get_initial(orders)
                formsets[answer_type] = _formset_factory(prefix=answer_type, initial=initial, data=self.data)
        return formsets

    def _get_initial(self, orders):
        return [dict(self.initial.items() + order.question.get_initial(order=order, country=self.initial['country']).items()) for order in orders]

    def is_valid(self):
        formset_checks = [formset.is_valid() for formset in self.formsets.values()]
        return len(formset_checks) == formset_checks.count(True)

    def save(self):
        for formset in self.formsets.values():
            for form in formset:
                self.form_answer_map.update({form: form.save()})
        self.assign_answer_groups()

    def show_is_required_errors(self):
        for formset in self.formsets.values():
            for form in formset:
                form.show_is_required_errors()

    def _highlight_required_answers(self, highlight):
        if highlight:
            self.show_is_required_errors()

    def assign_answer_groups(self):
        current_answer_form_counter = self.ANSWER_FORM_COUNTER
        self.ANSWER_FORM_COUNTER = self._initialize_form_counter()
        for subsection in self.section.sub_sections.all():
            for group in subsection.parent_question_groups():
                for order in group.question_orders():
                    if group.grid and group.display_all:
                        if order.question.is_primary:
                            for option in order.question.options.all():
                                answer_group = self._add_answer_to_group(order)
                                self._assign_non_primary_answers_to(answer_group, question_group=group)
                    else:
                        self._add_answer_to_group(order)
        self.ANSWER_FORM_COUNTER = current_answer_form_counter

    def _add_answer_to_group(self, order):
        form = self.next_ordered_form(order.question)
        answer = self.form_answer_map.get(form)
        row = AnswerGroup.next_row()
        if answer.answergroup.all().exists():
            return answer.answergroup.all()[0]
        return answer.answergroup.create(grouped_question=form.question_group, row=row)

    def _assign_non_primary_answers_to(self, answer_group, question_group):
        for question in question_group.all_non_primary_questions():
            form = self.next_ordered_form(question)
            answer_group.answer.add(self.form_answer_map.get(form))