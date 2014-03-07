from braces.views import MultiplePermissionsRequiredMixin
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views.generic import View
from questionnaire.forms.questionnaires import QuestionnaireFilterForm
from questionnaire.models import Organization, Questionnaire, Region


class ManageJRF(MultiplePermissionsRequiredMixin, View):
    permissions = {'any': ('auth.can_edit_questionnaire', 'auth.can_view_users')}

    def __init__(self, *args, **kwargs):
        super(ManageJRF, self).__init__(**kwargs)
        self.template_name = 'home/global/index.html'
        self.questionnaires = Questionnaire.objects.all().order_by('-year')

        self.who_regions = Region.objects.filter(organization__name='WHO').order_by('name')
        self.unicef_regions = Region.objects.filter(organization__name='UNICEF').order_by('name')

    def get(self, *args, **kwargs):
        context = {'finalized_questionnaires': self.questionnaires.filter(status=Questionnaire.FINALIZED),
                   'draft_questionnaires': self.questionnaires.filter(status=Questionnaire.DRAFT),
                   'filter_form': QuestionnaireFilterForm(),
                   'who_regions': self.who_regions,
                   'unicef_regions': self.unicef_regions,
                   'btn_label': 'Duplicate',
                   'action': reverse('duplicate_questionnaire_page')}
        return render(self.request, self.template_name, context)