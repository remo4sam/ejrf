from django import forms
from questionnaire.models import Questionnaire, Region
from questionnaire.services.questionnaire_cloner import QuestionnaireClonerService
from questionnaire.utils.form_utils import _set_year_choices


class QuestionnaireFilterForm(forms.Form):
    questionnaire = forms.ModelChoiceField(queryset=Questionnaire.objects.filter(status__in=[Questionnaire.FINALIZED, Questionnaire.PUBLISHED], region=None),
                                           empty_label="Select Questionnaire",
                                           widget=forms.Select(attrs={"class": 'form-control'}), required=True)
    year = forms.ChoiceField(widget=forms.Select(attrs={"class": 'form-control'}), required=True, choices=[])
    name = forms.CharField(widget=forms.HiddenInput(), required=True)

    def __init__(self, *args, **kwargs):
        super(QuestionnaireFilterForm, self).__init__(*args, **kwargs)
        self.fields['year'].choices = _set_year_choices()
        self.fields['year'].label = "Reporting Year"
        self.fields['questionnaire'].label = "Finalized Questionnaires"


class PublishQuestionnaireForm(forms.Form):
    regions = forms.ModelMultipleChoiceField(queryset=Region.objects.none(),
                                             widget=forms.CheckboxSelectMultiple(), required=True)

    def __init__(self, *args, **kwargs):
        super(PublishQuestionnaireForm, self).__init__(*args, **kwargs)
        self.fields['regions'].queryset = self._set_region_choices()

    def _set_region_choices(self):
        questionnaire = self.initial.get('questionnaire')
        regions = Region.objects.filter(organization__name="WHO")
        regions_with_questionnaire = Questionnaire.objects.filter(year=questionnaire.year, region__isnull=False).values_list('region', flat=True)
        return regions.exclude(id__in=regions_with_questionnaire)

    def save(self):
        regions = self.cleaned_data['regions']
        for region in regions:
            questionnaire = self.initial['questionnaire']
            QuestionnaireClonerService(questionnaire, region).clone()