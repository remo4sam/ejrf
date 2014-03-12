from braces.views import PermissionRequiredMixin
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, DeleteView

from questionnaire.forms.sections import SectionForm, SubSectionForm
from questionnaire.mixins import RegionAndPermissionRequiredMixin
from questionnaire.models import Section, SubSection
from questionnaire.utils.model_utils import reindex_orders_in


class NewSection(RegionAndPermissionRequiredMixin, CreateView):
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
        section.region = self.request.user.user_profile.region
        section.save()
        messages.success(self.request, "Section created successfully")
        return super(NewSection, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Section NOT created. See errors below.")
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
        self.object = None
        self.pk_url_kwarg = 'section_id'
        self.success_url = reverse("home_page")
        self.section = None

    def get_success_url(self):
        referer_url = self.request.META.get('HTTP_REFERER', None)
        section_page = reverse("questionnaire_entry_page", args=(self.section.questionnaire.id, self.section.id))
        deleting_myself = referer_url and (section_page in referer_url)
        if deleting_myself:
            return self.section.questionnaire.absolute_url()
        return referer_url

    def post(self, request, *args, **kwargs):
        self.section = self.get_object()
        response = super(DeleteSection, self).post(request, *args, **kwargs)
        reindex_orders_in(Section, questionnaire=self.section.questionnaire)
        message = "Section successfully deleted."
        messages.success(request, message)
        return response


class NewSubSection(RegionAndPermissionRequiredMixin, CreateView):
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
        self.section = Section.objects.get(id=section_id)
        self.form = SubSectionForm(instance=SubSection(section=self.section), data=request.POST)
        self.referer_url = reverse('questionnaire_entry_page', args=(questionnaire_id, section_id))
        if self.form.is_valid():
            return self._form_valid()
        return self._form_invalid()

    def _form_valid(self):
        subsection = self.form.save(commit=False)
        subsection.order = SubSection.get_next_order(self.section.id)
        subsection.region = self.request.user.user_profile.region
        subsection.save()
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


class DeleteSubSection(DeleteView):

    def __init__(self, **kwargs):
        super(DeleteSubSection, self).__init__(**kwargs)
        self.model = SubSection
        self.pk_url_kwarg = 'subsection_id'
        self.success_url = "/"

    def _set_success_url(self):
        self.object = self.get_object()
        section = self.object.section
        return section.get_absolute_url()

    def post(self, request, *args, **kwargs):
        self.success_url = self._set_success_url()
        response = super(DeleteSubSection, self).post(request, *args, **kwargs)
        reindex_orders_in(SubSection, section=self.object.section)
        message = "Subsection successfully deleted."
        messages.success(request, message)
        return response
