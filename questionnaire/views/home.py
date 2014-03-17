from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from django.core.urlresolvers import reverse
from braces.views import MultiplePermissionsRequiredMixin

from questionnaire.models import Questionnaire
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

        questionnaires = Questionnaire.objects.filter(status=Questionnaire.PUBLISHED, region__countries=self.request.user.user_profile.country)
        if questionnaires.exists():
            questionnaire = questionnaires.latest('created')
            args = (questionnaire.id, questionnaire.sections.all()[0].id)
            return HttpResponseRedirect(reverse('questionnaire_entry_page', args=args))
        return self._render_questionnaire_does_not_exist()

    def _render_questionnaire_does_not_exist(self):
        message = "Sorry, The JRF is not yet published at the moment"
        messages.error(self.request, message)
        return render(self.request, self.template_name)

    def _render_global_admin_view(self):
        status_map = QuestionnaireStatusService().region_country_status_map()
        return render(self.request, 'home/index.html', {'region_country_status_map': status_map})