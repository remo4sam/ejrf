from django.forms.formsets import formset_factory
from questionnaire.forms.answers import NumericalAnswerForm, TextAnswerForm, DateAnswerForm, MultiChoiceAnswerForm
from questionnaire.models import Question, AnswerGroup, QuestionGroupOrder


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
        self.mapped_question_orders = section.mapped_question_orders()
        self.formsets = self._formsets()
        self.ANSWER_FORM_COUNTER = self._initialize_form_counter()
        self._highlight_required_answers(highlight)
        self.form_answer_map = {}

    def next_ordered_form(self, question):
        next_question_type_count = self.ANSWER_FORM_COUNTER[question.answer_type]
        self.ANSWER_FORM_COUNTER[question.answer_type] += 1
        formset = self.formsets[question.answer_type][next_question_type_count]
        return formset

    @staticmethod
    def _initialize_form_counter():
        return {key: 0 for key in ANSWER_FORM.keys()}

    def _formsets(self):
        formsets = {}
        for answer_type in ANSWER_FORM.keys():
            mapped_orders = self.mapped_question_orders.get(answer_type)
            if mapped_orders:
                _formset_factory = formset_factory(ANSWER_FORM[answer_type], max_num=len(mapped_orders))
                initial = self._get_initial(mapped_orders)
                formsets[answer_type] = _formset_factory(prefix=answer_type, initial=initial, data=self.data)
        return formsets

    def _initial(self, order_dict):
        option = order_dict.get('option', None)
        order = order_dict.get('order', None)
        country = self.initial.get('country')
        version = self.initial.get('version')
        question = order.question
        question_group = order.question_group

        initial = {'question': question, 'group': question_group, 'country': country}

        answer = None
        if option:
            primary_answer = option.answer.filter(version=version)
            if question.is_primary:
                initial['option'] = option
                answer = primary_answer
            elif primary_answer.exists():
                answer_group = primary_answer[0].answergroup.filter(grouped_question=question_group)
                answer = answer_group[0].answer.filter(question=order.question).select_subclasses()
        else:
            answer = question.answers.filter(answergroup__grouped_question=question_group,
                                             country=country, version=version).select_subclasses()
        if answer:
            self._append(answer, initial)
        return dict(self.initial.items() + initial.items())

    def _append(self, answer, initial):
        answer = answer.latest('modified')
        initial['response'] = answer.format_response()
        if answer.is_draft():
            initial['answer'] = answer

    def _get_initial(self, orders):
        return [self._initial(order_dict=order) for order in orders]

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