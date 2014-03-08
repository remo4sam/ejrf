from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import FormView
from django.views.generic import View
from braces.views import MultiplePermissionsRequiredMixin, LoginRequiredMixin
from questionnaire.forms.questionnaires import QuestionnaireFilterForm, PublishQuestionnaireForm

from questionnaire.forms.sections import SectionForm, SubSectionForm
from questionnaire.services.questionnaire_cloner import QuestionnaireClonerService
from questionnaire.services.questionnaire_finalizer import QuestionnaireFinalizeService
from questionnaire.services.questionnaire_entry_form_service import QuestionnaireEntryFormService
from questionnaire.models import Questionnaire, Section
from questionnaire.forms.answers import NumericalAnswerForm, TextAnswerForm, DateAnswerForm, MultiChoiceAnswerForm
from questionnaire.services.users import UserQuestionnaireService


ANSWER_FORM = {'Number': NumericalAnswerForm,
               'Text': TextAnswerForm,
               'Date': DateAnswerForm,
               'MultiChoice': MultiChoiceAnswerForm,
               }


class Entry(MultiplePermissionsRequiredMixin, FormView):
    template_name = 'questionnaires/entry/index.html'
    permissions = {'any': ('auth.can_submit_responses', 'auth.can_view_users', 'auth.can_edit_questionnaire')}

    def get(self, request, *args, **kwargs):
        questionnaire = Questionnaire.objects.get(id=self.kwargs['questionnaire_id'])
        section = Section.objects.get(id=self.kwargs['section_id'])
        user_questionnaire_service = UserQuestionnaireService(self.request.user, questionnaire)
        initial = {'status': 'Draft', 'country': self.request.user.user_profile.country, 'version': user_questionnaire_service.GET_version}
        required_answers = 'show' in request.GET
        formsets = QuestionnaireEntryFormService(section, initial=initial, highlight=required_answers)

        printable = 'printable' in request.GET
        preview = user_questionnaire_service.preview() or 'preview' in request.GET

        context = {'questionnaire': questionnaire,
                   'section': section, 'printable': printable,
                   'preview': preview, 'formsets': formsets,
                   'ordered_sections': questionnaire.sections.order_by('order'),
                   'form': SectionForm(initial={'questionnaire': questionnaire}),
                   'action': reverse('new_section_page', args=(questionnaire.id, )),
                   'subsection_form': SubSectionForm(),
                   'subsection_action': reverse('new_subsection_page', args=(questionnaire.id, section.id))}

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        questionnaire = Questionnaire.objects.get(id=self.kwargs['questionnaire_id'])
        section = Section.objects.get(id=self.kwargs['section_id'])
        user_questionnaire_service = UserQuestionnaireService(self.request.user, questionnaire)
        initial = {'country': self.request.user.user_profile.country, 'status': 'Draft',
                   'version': user_questionnaire_service.POST_version}
        formsets = QuestionnaireEntryFormService(section, initial=initial, data=request.POST)

        context = {'questionnaire': questionnaire, 'section': section,
                   'formsets': formsets, 'ordered_sections': Section.objects.order_by('order')}

        if formsets.is_valid():
            return self._form_valid(request, formsets, user_questionnaire_service, context)
        return self._form_invalid(request, context)

    def _form_valid(self, request, formsets, user_questionnaire_service, context):
        formsets.save()
        message = 'Draft saved.'
        messages.success(request, message)
        if request.POST.get('redirect_url', None):
            return HttpResponseRedirect(request.POST['redirect_url'].replace('preview=1', ''))
        return self.render_to_response(context)

    def _form_invalid(self, request, context):
        message = 'Draft NOT saved. See errors below.'
        messages.error(request, message)
        return self.render_to_response(context)


class SubmitQuestionnaire(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        questionnaire = Questionnaire.objects.get(status=Questionnaire.PUBLISHED)
        user_questionnaire = UserQuestionnaireService(self.request.user, questionnaire)
        if not user_questionnaire.required_sections_answered():
            return self._reload_section_with_required_answers_errors(request, user_questionnaire, *args, **kwargs)
        return self._submit_answers(request, user_questionnaire, *args, **kwargs)

    def _submit_answers(self, request, user_questionnaire_service, *args, **kwargs):
        user_questionnaire_service.submit()
        referer_url = request.META.get('HTTP_REFERER', None)
        redirect_url = referer_url or reverse('home_page')
        redirect_url = self._format_redirect_url(redirect_url)
        messages.success(request, 'Questionnaire Submitted.')
        return HttpResponseRedirect(redirect_url)

    def _reload_section_with_required_answers_errors(self, request, user_questionnaire_service, *args, **kwargs):
        section = user_questionnaire_service.unanswered_section
        questionnaire = user_questionnaire_service.questionnaire
        messages.error(request, 'Questionnaire NOT submitted. See errors below.')
        redirect_url = reverse('questionnaire_entry_page', args=(questionnaire.id, section.id))
        return HttpResponseRedirect('%s?show=errors' % redirect_url)

    def _format_redirect_url(self, redirect_url):
        redirect_url = redirect_url.replace('?show=errors', '')
        return "%s?preview=1" % redirect_url


class DuplicateQuestionnaire(View):
    def post(self, *args, **kwargs):
        form = QuestionnaireFilterForm(self.request.POST)
        if form.is_valid():
            duplicate, _ = QuestionnaireClonerService(form.cleaned_data['questionnaire']).clone()
            duplicate.name = form.cleaned_data['name']
            duplicate.year = form.cleaned_data['year']
            duplicate.save()
            message = "The questionnaire has been duplicated successfully, You can now go ahead and edit it"
            messages.success(self.request, message)
            redirect_url = reverse('questionnaire_entry_page', args=(duplicate.id, duplicate.sections.all()[0].id))
            return HttpResponseRedirect(redirect_url)
        message = "Questionnaire could not be duplicated see errors below"
        messages.error(self.request, message)
        return HttpResponseRedirect(reverse('manage_jrf_page'))


class FinalizeQuestionnaire(View):
    def post(self, request, *args, **kwargs):
        questionnaire = Questionnaire.objects.get(id=kwargs['questionnaire_id'])
        QuestionnaireFinalizeService(questionnaire).finalize()
        message = "The questionnaire has been finalized successfully."
        messages.success(self.request, message)
        return HttpResponseRedirect(reverse('manage_jrf_page'))


class UnfinalizeQuestionnaire(View):
    def post(self, request, *args, **kwargs):
        questionnaire = Questionnaire.objects.get(id=kwargs['questionnaire_id'])
        QuestionnaireFinalizeService(questionnaire).unfinalize()
        message = "The questionnaire is now in progress."
        messages.success(self.request, message)
        return HttpResponseRedirect(reverse('manage_jrf_page'))


class PublishQuestionnaire(View):
    template_name = 'questionnaires/_publish.html'

    def get(self, *args, **kwargs):
        questionnaire = Questionnaire.objects.get(id=self.kwargs['questionnaire_id'])
        form = PublishQuestionnaireForm(initial={'questionnaire': questionnaire})
        context = {'questionnaire': questionnaire, 'publish_form': form, 'btn_label': "Publish"}
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        questionnaire = Questionnaire.objects.get(id=self.kwargs['questionnaire_id'])
        form = PublishQuestionnaireForm(initial={'questionnaire': questionnaire}, data=self.request.POST)
        if form.is_valid():
            form.save()
            message = "The questionnaire has been published to %s" % ", ".join([region.name for region in form.cleaned_data['regions']])
            messages.success(self.request, message)
        else:
            message = "Questionnaire could not be published see errors below"
            messages.error(self.request, message)
        return HttpResponseRedirect(reverse('manage_jrf_page'))
