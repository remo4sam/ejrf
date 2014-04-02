import copy
from django.forms.formsets import formset_factory
from questionnaire.forms.answers import NumericalAnswerForm, TextAnswerForm, DateAnswerForm, MultiChoiceAnswerForm
from questionnaire.models import AnswerGroup, Answer, NumericalAnswer, TextAnswer, DateAnswer, MultiChoiceAnswer, QuestionOption
from questionnaire.utils.questionnaire_entry_helpers import extra_rows, clean_data_dict

EMPTY_ROW = ['']

ANSWER_FORM = {
    'Number': NumericalAnswerForm,
    'Text': TextAnswerForm,
    'Date': DateAnswerForm,
    'MultiChoice': MultiChoiceAnswerForm
}


class QuestionnaireEntryFormService(object):

    def __init__(self, section, initial={}, data=None, highlight=False, edit_after_submit=False):
        self.initial = initial
        self.data = data
        self.cleaned_data = clean_data_dict(dict(copy.deepcopy(data))) if data else None
        self.section = section
        self.mapped_question_orders = section.mapped_question_orders()
        self.country = self.initial.get('country')
        self.version = self.initial.get('version')
        self.questionnaire = self.initial.get('questionnaire')
        self.extra_rows = {}
        self.formsets = self._formsets()
        self.ANSWER_FORM_COUNTER = self._initialize_form_counter()
        self._highlight_required_answers(highlight)
        self.form_answer_map = {}
        self.editing_after_submit = edit_after_submit

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
                initial = self._get_initial(mapped_orders,  answer_type)
                _formset_factory = formset_factory(ANSWER_FORM[answer_type], max_num=len(initial))
                formsets[answer_type] = _formset_factory(prefix=answer_type, initial=initial, data=self.data)
        return formsets

    def _initial(self, order_dict):
        option = order_dict.get('option', None)
        order = order_dict.get('order', None)
        question = order.question
        question_group = order.question_group
        initial = {'question': question, 'group': question_group, 'country': self.country,
                   'questionnaire': self.questionnaire}
        answer = None
        if option:
            primary_answer = Answer.from_response(response=option, version=self.version, country=self.country,
                                              questionnaire=self.questionnaire)

            if question.is_primary:
                if question_group.display_all:
                    initial['option'] = option
                answer = primary_answer
            elif primary_answer.exists():
                answer_group = primary_answer[0].answergroup.filter(grouped_question=question_group)
                if answer_group:
                    answer = answer_group[0].answer.filter(question=order.question, country=self.country,
                                                           version=self.version,
                                                           questionnaire=self.questionnaire).select_subclasses()
        else:
            answer = question.answers.filter(answergroup__grouped_question=question_group, country=self.country,
                                             version=self.version,
                                             questionnaire=self.questionnaire).select_subclasses()
        if answer:
            self._append(answer, initial)
        return dict(self.initial.items() + initial.items())

    def _append(self, answer, initial):
        answer = answer.latest('modified')
        initial['response'] = answer.format_response()
        if answer.is_draft():
            initial['answer'] = answer

    def _get_initial(self, orders, answer_type):
        initial =[]
        for order_dict in orders:
            order = order_dict['order']
            group = order.question_group
            if group.allow_multiples:
                if order.is_first_answer_type_in_group():
                    row_numbers = self.get_extra_rows(answer_type, group)
                    self.extra_rows[group] = row_numbers
                    questions = group.ordered_questions()
                    question_orders = filter(lambda order: self._order_in(order['order'], group, questions), orders)
                    for row_number in row_numbers:
                        self._update(row_number, question_orders, initial)
            else:
                initial.append(self._initial(order_dict=order_dict))

        return initial

    def _order_in(self, order, group, questions):
        return order.question_group == group and order.question in questions

    def _update(self, row_number, question_orders, initial):
        for order_dict in question_orders:
            initial.append(self._initial({'option': row_number, 'order': order_dict['order']}))

    def get_extra_rows(self, answer_type, group):
        if self.cleaned_data:
            rows = extra_rows(self.cleaned_data, answer_type, group.id)
            return EMPTY_ROW * len(rows)
        primary_question = group.primary_question()[0]
        options = primary_question.answered_options(questionnaire=self.questionnaire, country=self.country,
                                                    question_group=group, version=self.version)
        return options or EMPTY_ROW

    def is_valid(self):
        formset_checks = [formset.is_valid() for formset in self.formsets.values()]
        return len(formset_checks) == formset_checks.count(True)

    def save(self):
        if self.editing_after_submit:
            self._duplicate_other_sections_answers_and_answer_groups()
        self._save_current_section()

    def _duplicate_other_sections_answers_and_answer_groups(self):
        version_ = self.initial['version']
        answer_groups = AnswerGroup.objects.filter(answer__questionnaire=self.section.questionnaire,
                                                   answer__country=self.initial['country'],
                                                   answer__version=version_-1).exclude(
            grouped_question__subsection__section=self.section).distinct().select_related()
        for answer_group in answer_groups:
            new_answer_group = AnswerGroup.objects.create(grouped_question=answer_group.grouped_question, row=answer_group.row)
            for answer in answer_group.answer.all().select_related().select_subclasses():
                new_answer = eval(answer.__class__.__name__).objects.create(question=answer.question, country=answer.country, code=answer.code,
                                                                            response=answer.response, version=version_, status=Answer.DRAFT_STATUS,
                                                                            questionnaire=answer.questionnaire)
                new_answer_group.answer.add(new_answer)

    def _save_current_section(self):
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
                    elif group.grid and group.allow_multiples:
                        if order.question.is_primary:
                            for option in extra_rows(self.cleaned_data, order.question.answer_type, group.id):
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