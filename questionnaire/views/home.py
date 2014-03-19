from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from django.core.urlresolvers import reverse
from braces.views import MultiplePermissionsRequiredMixin

from questionnaire.models import Questionnaire, Answer
from questionnaire.services.questionnaire_status import QuestionnaireStatusService


class Home(MultiplePermissionsRequiredMixin, View):
    def __init__(self, *args, **kwargs):
        super(Home, self).__init__(*args, **kwargs)
        self.permissions = {'any': ('auth.can_submit_responses', 'auth.can_view_users', 'auth.can_edit_questionnaire')}
        self.template_name = "home/index.html"

    def get(self, *args, **kwargs):
        if self.request.user.has_perm('auth.can_view_users'):
            return self._render_global_admin_view()
        if self.request.user.has_perm('auth.can_edit_questionnaire') and self.request.user.user_profile.region:
            region = self.request.user.user_profile.region
            return HttpResponseRedirect(reverse('manage_regional_jrf_page', args=(region.id,)))
        return self._render_submitter_view()

    def _render_questionnaire_does_not_exist(self):
        message = "Sorry, The JRF is not yet published at the moment"
        messages.error(self.request, message)
        return render(self.request, self.template_name)

    def _render_global_admin_view(self):
        status_map = QuestionnaireStatusService().region_country_status_map()
        return render(self.request, 'home/index.html', {'region_country_status_map': status_map})

    def _render_submitter_view(self):
        country = self.request.user.user_profile.country
        un_answered, submitted, drafts = self._get_questionnaires(country)
        context = {'drafts': country.get_versions_for(drafts),
                   'new': country.get_versions_for(un_answered),
                   'submitted': country.get_versions_for(submitted)}
        return render(self.request, 'home/submitter/index.html', context)

    def _get_questionnaires(self, country):
        questionnaires = Questionnaire.objects.filter(region__countries=country, status=Questionnaire.PUBLISHED)
        drafts = questionnaires.filter(sections__sub_sections__question_group__question__answers__status=Answer.DRAFT_STATUS)
        submitted = questionnaires.filter(sections__sub_sections__question_group__question__answers__status=Answer.SUBMITTED_STATUS).exclude(id__in=drafts.values_list('id', flat=True))
        un_answered = questionnaires.exclude(Q(id__in=drafts.values_list('id', flat=True)) | Q(id__in=submitted.values_list('id', flat=True)))
        return un_answered, submitted, drafts