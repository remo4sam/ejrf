from django.forms import ModelForm
from questionnaire.models import Theme


class ThemeForm(ModelForm):
    class Meta:
        model = Theme
        fields = ['name', 'description']