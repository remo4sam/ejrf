from braces.views import PermissionRequiredMixin
from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from questionnaire.forms.theme import ThemeForm
from questionnaire.models import Theme


class ThemeList(PermissionRequiredMixin, ListView):
    model = Theme
    template_name = "themes/index.html"
    permission_required = 'auth.can_edit_questionnaire'

    def get_context_data(self, **kwargs):
        context = super(ThemeList, self).get_context_data(**kwargs)
        context.update({'theme_form': ThemeForm(), 'theme_form_action': reverse('new_theme_page')})
        return context


class NewTheme(PermissionRequiredMixin, CreateView):
    model = Theme
    success_url = reverse_lazy('theme_list_page')
    template_name = "themes/new.html"
    permission_required = 'auth.can_edit_questionnaire'

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


class EditTheme(PermissionRequiredMixin, UpdateView):
    model = Theme
    pk_url_kwarg = 'theme_id'
    success_url = reverse_lazy('theme_list_page')
    template_name = "themes/new.html"
    permission_required = 'auth.can_edit_questionnaire'

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


class DeleteTheme(PermissionRequiredMixin, DeleteView):
    model = Theme
    pk_url_kwarg = 'theme_id'
    success_url = reverse_lazy('theme_list_page')
    template_name = "themes/index.html"
    permission_required = 'auth.can_edit_questionnaire'

    def delete(self, request, *args, **kwargs):
        theme_to_delete = self.model.objects.get(id=kwargs['theme_id'])
        theme_to_delete.de_associate_questions()
        response = super(DeleteTheme, self).delete(request, *args, **kwargs)
        message = "Theme successfully deleted."
        messages.success(self.request, message)
        return response