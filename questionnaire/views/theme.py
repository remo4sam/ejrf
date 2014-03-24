from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
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
    success_url = reverse_lazy('theme_list_page')
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


class EditTheme(UpdateView):
    model = Theme
    pk_url_kwarg = 'theme_id'
    success_url = reverse_lazy('theme_list_page')
    template_name = "themes/new.html"

    def form_valid(self, form):
        response = super(EditTheme, self).form_valid(form)
        message = "Theme successfully updated."
        messages.success(self.request, message)
        return response

    def form_invalid(self, form):
        response = super(EditTheme, self).form_invalid(form)
        message = "Theme was not updated, see Errors below"
        messages.error(self.request, message)
        return response