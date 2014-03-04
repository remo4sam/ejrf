from django.forms import ModelForm
from django import forms
from questionnaire.models import Section, SubSection


class SectionForm(ModelForm):

    class Meta:
        model = Section
        fields = ['questionnaire', 'name', 'title', 'description']
        widgets = {'questionnaire': forms.HiddenInput(),
                   'description': forms.Textarea(attrs={"rows": 4, "cols": 40})}


class SubSectionForm(ModelForm):

    def save(self, commit=True, *args, **kwargs):
        subsection = super(SubSectionForm, self).save(commit=False, *args, **kwargs)
        if not self.instance.order:
            subsection.order = SubSection.get_next_order(self.instance.section.id)
        if commit:
            subsection.save()
        return subsection

    class Meta:
        model = SubSection
        fields = ['title', 'description']
        widgets = {'description': forms.Textarea(attrs={"rows": 4, "cols": 50})}