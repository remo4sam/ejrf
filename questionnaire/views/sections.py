from braces.views import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, request
from django.views.generic import CreateView, View, UpdateView, DeleteView

from questionnaire.forms.sections import SectionForm, SubSectionForm
from questionnaire.models import Section, SubSection, Questionnaire


class NewSection(PermissionRequiredMixin, CreateView):
    permission_required = 'auth.can_edit_questionnaire'

    def __init__(self, **kwargs):
        super(NewSection, self).__init__(**kwargs)
        self.form_class = SectionForm
        self.object = Section
        self.template_name = "sections/subsections/new.html"

    def get_context_data(self, **kwargs):
        context = super(NewSection, self).get_context_data(**kwargs)
        context['btn_label'] = "CREATE"
        return context

    def form_valid(self, form):
        section = form.save(commit=False)
        section.order = Section.get_next_order(form.cleaned_data['questionnaire'])
        section.save()
        messages.success(self.request,"Section created successfully" )
        return super(NewSection, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request,"Section NOT created. See errors below." )
        context = {'id':  "new-section-modal",
                   'form': form, 'btn_label': "CREATE", }
        return self.render_to_response(context)


class EditSection(PermissionRequiredMixin, UpdateView):
    permission_required = 'auth.can_edit_questionnaire'

    def __init__(self, *args, **kwargs):
        super(EditSection, self).__init__(*args, **kwargs)
        self.form_class = SectionForm
        self.model = Section
        self.template_name = "sections/subsections/new.html"
        self.pk_url_kwarg = 'section_id'

    def get_context_data(self, **kwargs):
        context = super(EditSection, self).get_context_data(**kwargs)
        context['btn_label'] = "SAVE"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Section updated successfully.")
        return super(EditSection, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Section NOT updated. See errors below." )
        return super(EditSection, self).form_invalid(form)


class DeleteSection(DeleteView):

    def __init__(self, *args, **kwargs):
        super(DeleteSection, self).__init__(*args, **kwargs)
        self.model = Section
        self.pk_url_kwarg = 'section_id'
        self.success_url = reverse("home_page")

    def _set_success_url(self, request):
        referer_url = request.META.get('HTTP_REFERER', None)
        home_page = reverse("home_page")
        self.object = self.get_object()
        section_page = reverse("questionnaire_entry_page", args=(self.object.questionnaire.id, self.object.id))
        if referer_url and section_page in referer_url:
            return home_page
        return referer_url or home_page

    def post(self, request, *args, **kwargs):
        self.success_url = self._set_success_url(request)
        message = "Section successfully deleted."
        messages.success(request, message)
        return super(DeleteSection, self).post(request, *args, **kwargs)


class NewSubSection(PermissionRequiredMixin, CreateView):
    permission_required = 'auth.can_edit_questionnaire'

    def __init__(self, **kwargs):
        super(NewSubSection, self).__init__(**kwargs)
        self.object = SubSection
        self.form_class = SubSectionForm
        self.template_name = "sections/subsections/new.html"

    def get_context_data(self, **kwargs):
        context = super(NewSubSection, self).get_context_data(**kwargs)
        context['btn_label'] = "CREATE"
        return context

    def post(self, request, *args, **kwargs):
        questionnaire_id = kwargs.get('questionnaire_id')
        section_id = kwargs.get('section_id')
        section = Section.objects.get(id=section_id)
        self.form = SubSectionForm(instance=SubSection(section=section), data=request.POST)
        self.referer_url = reverse('questionnaire_entry_page', args=(questionnaire_id, section_id))
        if self.form.is_valid():
            return self._form_valid()
        return self._form_invalid()

    def _form_valid(self):
        self.form.save()
        messages.success(self.request, "Subsection successfully created." )
        return HttpResponseRedirect(self.referer_url)

    def _form_invalid(self):
        messages.error(self.request, "Subsection NOT created. See errors below." )
        context = {'id':  "new-subsection-modal",
                   'form': self.form, 'btn_label': "CREATE", }
        return self.render_to_response(context)


class EditSubSection(PermissionRequiredMixin, UpdateView):
    permission_required = 'auth.can_edit_questionnaire'

    def __init__(self, *args, **kwargs):
        super(EditSubSection, self).__init__(*args, **kwargs)
        self.form_class = SubSectionForm
        self.model = SubSection
        self.template_name = "sections/subsections/new.html"
        self.pk_url_kwarg = 'subsection_id'

    def get_context_data(self, **kwargs):
        context = super(EditSubSection, self).get_context_data(**kwargs)
        context['btn_label'] = "SAVE"
        return context

    def form_valid(self, form):
        messages.success(self.request, "SubSection updated successfully.")
        return super(EditSubSection, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "SubSection NOT updated. See errors below.")
        return super(EditSubSection, self).form_invalid(form)