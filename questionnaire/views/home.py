from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from django.core.urlresolvers import reverse
from braces.views import MultiplePermissionsRequiredMixin

from questionnaire.models import Questionnaire


class Home(MultiplePermissionsRequiredMixin, View):
    def __init__(self, *args, **kwargs):
        super(Home, self).__init__(*args, **kwargs)
        self.permissions = {'any': ('auth.can_submit_responses', 'auth.can_view_users')}
        self.template_name = "home/index.html"
        self.questionnaires = Questionnaire.objects.filter(status=Questionnaire.PUBLISHED)

    def get(self, *args, **kwargs):
        if self.request.user.has_perm('auth.can_view_users'):
            return HttpResponseRedirect(reverse('manage_jrf_page'))
        if self.questionnaires.exists():
            return self._render_questionnaire_section()
        return self._render_questionnaire_does_not_exist()

    def _render_questionnaire_does_not_exist(self):
        message = "Sorry, There are no published questionnaires at the moment"
        messages.error(self.request, message)
        return render(self.request, self.template_name)

    def _render_questionnaire_section(self):
        questionnaire = self.questionnaires.latest('created')
        args = (questionnaire.id, questionnaire.sections.all()[0].id)
        return HttpResponseRedirect(reverse('questionnaire_entry_page', args=args))