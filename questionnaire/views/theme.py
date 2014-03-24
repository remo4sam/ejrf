from django.contrib import messages
from django.core.urlresolvers import reverse
from django.views.generic import ListView, CreateView
from questionnaire.forms.theme import ThemeForm
from questionnaire.models import Theme


class ThemeList(ListView):
    model = Theme
    template_name = "themes/index.html"

    def get_context_data(self, **kwargs):
        context = super(ThemeList, self).get_context_data(**kwargs)
        context.update({'theme_form': ThemeForm(), 'theme_form_action': reverse('new_theme_page')})
        return context


class NewTheme(CreateView):
    model = Theme
    success_url = "/themes/"
    template_name = "themes/new.html"

    def form_valid(self, form):
        response = super(NewTheme, self).form_valid(form)
        message = "Theme successfully created."
        messages.success(self.request, message)
        return response

    def form_invalid(self, form):
        response = super(NewTheme, self).form_invalid(form)
        message = "Theme was not created, see Errors below"
        messages.error(self.request, message)
        return response