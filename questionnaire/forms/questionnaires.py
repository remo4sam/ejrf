from datetime import date
from django import forms
from questionnaire.models import Questionnaire


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


class QuestionnairePublishFilterForm(forms.Form):
    pass