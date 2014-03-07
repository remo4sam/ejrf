from datetime import date
from django import forms
from django.forms import ModelForm
from questionnaire.models import Questionnaire, Region
from questionnaire.services.questionnaire_cloner import QuestionnaireClonerService


class QuestionnaireFilterForm(forms.Form):
    questionnaire = forms.ModelChoiceField(queryset=Questionnaire.objects.filter(status=Questionnaire.FINALIZED),
                                           empty_label="Select Questionnaire",
                                           widget=forms.Select(attrs={"class": 'form-control'}), required=True)
    year = forms.ChoiceField(widget=forms.Select(attrs={"class": 'form-control'}), required=True, choices=[])
    name = forms.CharField(widget=forms.HiddenInput(), required=True)

    def __init__(self, *args, **kwargs):
        super(QuestionnaireFilterForm, self).__init__(*args, **kwargs)
        self.fields['year'].choices = self._set_year_choices()
        self.fields['year'].label = "Reporting Year"
        self.fields['questionnaire'].label = "Finalized Questionnaires"

    def _set_year_choices(self):
        choices = []
        choices.insert(0, ('', 'Choose a year', ))
        questionnaire_years = Questionnaire.objects.all().values_list('year', flat=True)
        ten_year_range = [date.today().year + count for count in range(0, 10)]
        all_years = filter(lambda year: year not in questionnaire_years, ten_year_range)
        choices.extend((year, year) for year in list(all_years))
        return choices


class PublishQuestionnaireForm(forms.Form):
    regions = forms.ModelMultipleChoiceField(queryset=Region.objects.none(),
                                             widget=forms.CheckboxSelectMultiple(attrs={"class": 'form-control'}), required=True)

    def __init__(self, *args, **kwargs):
        super(PublishQuestionnaireForm, self).__init__(*args, **kwargs)

        print self._set_region_choices()
        self.fields['regions'].queryset = self._set_region_choices()
        print self._set_region_choices()
        print self.fields

    def _set_region_choices(self):
        questionnaire = self.initial.get('questionnaire', None)
        regions = Region.objects.all()
        regions_with_questionnaire = Questionnaire.objects.filter(year=questionnaire.year, region__isnull=False).values_list('region', flat=True)
        if questionnaire:
            return regions.exclude(id__in=regions_with_questionnaire)
        return regions

    def save(self):
        regions = self.cleaned_data['regions']
        for region in regions:
            QuestionnaireClonerService(self.initial['questionnaire'], region).clone()