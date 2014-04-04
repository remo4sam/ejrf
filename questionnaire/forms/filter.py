from django import forms
from django.contrib.auth.models import Group
from questionnaire.models import Region, Organization, Country, Theme, Questionnaire


class UserFilterForm(forms.Form):
    organization = forms.ModelChoiceField(queryset=Organization.objects.order_by('name'),
                                          empty_label="All",
                                          widget=forms.Select(attrs={"class": 'form-control region-select'}),
                                          required=False)
    region = forms.ModelChoiceField(queryset=Region.objects.all(), empty_label="All",
                                    widget=forms.Select(attrs={"class": 'form-control region-select'}), required=False)
    role = forms.ModelChoiceField(queryset=Group.objects.order_by('name'), empty_label="All",
                                  widget=forms.Select(attrs={"class": 'form-control region-select'}), required=False)


class ExportFilterForm(forms.Form):
    regions = forms.ModelMultipleChoiceField(queryset=Region.objects.all(),
                                             widget=forms.CheckboxSelectMultiple(), required=False)
    countries = forms.ModelMultipleChoiceField(queryset=Country.objects.order_by('name'),
                                               widget=forms.CheckboxSelectMultiple(), required=False)
    themes = forms.ModelMultipleChoiceField(queryset=Theme.objects.order_by('name'),
                                            widget=forms.CheckboxSelectMultiple(), required=False)
    year = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), required=False, choices=[])

    def __init__(self, *args, **kwargs):
        super(ExportFilterForm, self).__init__(*args, **kwargs)
        self.fields['year'].choices = self._set_year_choices()

    @staticmethod
    def _set_year_choices():
        choices = []
        years_with_questionnaires = set(Questionnaire.objects.all().values_list('year', flat=True))
        choices.extend((year, year) for year in list(years_with_questionnaires))
        return choices