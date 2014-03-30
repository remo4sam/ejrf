from django import forms
from django.forms.util import ErrorDict
from django.forms import ModelForm, ModelChoiceField
from django.utils.html import format_html
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe

from questionnaire.models import NumericalAnswer, TextAnswer, DateAnswer, MultiChoiceAnswer


class AnswerForm(ModelForm):
    def __init__(self,  *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        self.question = self._get_question(kwargs)
        self.fields['response'].required = self.question.is_required
        self._initial = self._set_initial(kwargs)
        self.is_editing = False
        self._set_instance()
        self.question_group = self._initial['group'] if self._initial else None

    def _set_initial(self, kwargs):
        initial = kwargs['initial'] if 'initial' in kwargs else {}
        if self.data and 'response' and self.data.keys():
            if 'response' in initial.keys():
                del initial['response']
        return initial

    def _set_instance(self):
        if 'answer' in self._initial:
            self.is_editing = True
            self.instance = self._initial['answer']

    def show_is_required_errors(self):
        if self.question.is_required and not self.data and not self._initial.get('response', None):
            self._errors = self._errors or ErrorDict()
            self._errors['response'] = self.error_class(['This field is required.'])

    def save(self, commit=True, *args, **kwargs):
        if self.is_editing:
            return super(AnswerForm, self).save(commit=commit, *args, **kwargs)
        return self._create_new_answer(*args, **kwargs)

    def _create_new_answer(self, *args, **kwargs):
        answer = super(AnswerForm, self).save(commit=False, *args, **kwargs)
        self._add_extra_attributes_to(answer)
        answer.save()
        return answer

    def _add_extra_attributes_to(self, answer):
        for attribute in self._initial.keys():
            setattr(answer, attribute, self._initial[attribute])

    def _get_question(self, kwargs):
        return kwargs['initial'].get('question', None)


class NumericalAnswerForm(AnswerForm):
    class Meta:
        model = NumericalAnswer
        exclude = ('question', 'status', 'country', 'version', 'code', 'questionnaire')


class TextAnswerForm(AnswerForm):
    response = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = TextAnswer
        exclude = ('question', 'status', 'country', 'version', 'code', 'questionnaire')


class DateAnswerForm(AnswerForm):
    class Meta:
        model = DateAnswer
        exclude = ('question', 'status', 'country', 'version', 'code', 'questionnaire')
        widgets = {
            'response': forms.DateInput(attrs={'class': 'form-control datetimepicker', 'data-format':'YYYY-MM-DD'})
        }


class MultiChoiceAnswerSelectWidget(forms.Select):
    def __init__(self, attrs=None, choices=(), question_options=None):
        super(MultiChoiceAnswerSelectWidget, self).__init__(attrs, choices)
        self.question_options = question_options

    def render_option(self, selected_choices, option_value, option_label):
        option_value = force_text(option_value)
        data_instruction = ''
        if option_value:
            data_instruction = mark_safe(' data-instructions="%s"' % self.question_options.get(id=int(option_value)).instructions)
        if option_value in selected_choices:
            selected_html = mark_safe(' selected="selected"')
        else:
            selected_html = ''
        return format_html('<option value="{0}"{1}{2}>{3}</option>',
                           option_value,
                           selected_html,
                           data_instruction,
                           force_text(option_label))


class MultiChoiceAnswerForm(AnswerForm):
    response = ModelChoiceField(queryset=None, widget=forms.Select())

    def __init__(self, *args, **kwargs):
        super(MultiChoiceAnswerForm, self).__init__(*args, **kwargs)
        query_set = self._get_response_choices(kwargs)
        self.fields['response'].widget = self._get_response_widget(query_set)
        self.fields['response'].queryset = query_set
        self.fields['response'].empty_label = self._set_response_label(query_set)

    def _set_response_label(self, query_set):
        if self.widget_is_radio_button(query_set) or query_set.count()==1:
            return None
        return "Choose One"

    def widget_is_radio_button(self, query_set):
        if self._initial['group'].grid:
            return False
        return query_set.count() == 2 or query_set.filter(text='Yes').exists() or query_set.filter(text='Male').exists()

    def _get_response_widget(self, query_set):
        if self.widget_is_radio_button(query_set):
            return forms.RadioSelect()
        if query_set.exclude(instructions=None).exists():
            return MultiChoiceAnswerSelectWidget(question_options=query_set)
        return forms.Select()

    def _get_response_choices(self, kwargs):
        all_options = self.question.options.all()
        if 'option' in self._initial:
            return all_options.filter(id=self._initial.get('option').id)
        return all_options

    class Meta:
        model = MultiChoiceAnswer
        exclude = ('question', 'status', 'country', 'version', 'code', 'questionnaire')