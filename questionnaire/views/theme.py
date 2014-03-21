from django.shortcuts import render_to_response
from django.views.generic import ListView
from questionnaire.models import Theme


class ThemeList(ListView):
    model = Theme
    template_name = "themes/index.html"
