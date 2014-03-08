from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views.generic import View
from braces.views import MultiplePermissionsRequiredMixin
from questionnaire.forms.questionnaires import QuestionnaireFilterForm
from questionnaire.models import Questionnaire, Region


class ManageJRF(MultiplePermissionsRequiredMixin, View):
    permissions = {'any': ('auth.can_edit_questionnaire', 'auth.can_view_users')}

    def __init__(self, *args, **kwargs):
        super(ManageJRF, self).__init__(**kwargs)
        self.template_name = 'home/global/index.html'
        self.questionnaires = Questionnaire.objects.all().order_by('-year')
        self.regions = Region.objects.filter(organization__name='WHO').order_by('name')

    def get(self, *args, **kwargs):
        core_questionnaires = self.questionnaires.filter(region__isnull=True)
        context = {'finalized_questionnaires': core_questionnaires.filter(status=Questionnaire.FINALIZED),
                   'draft_questionnaires': core_questionnaires.filter(status=Questionnaire.DRAFT),
                   'filter_form': QuestionnaireFilterForm(),
                   'regions_questionnaire_map': self.map_region_with_questionnaires(),
                   'btn_label': 'Duplicate',
                   'action': reverse('duplicate_questionnaire_page')}
        return render(self.request, self.template_name, context)

    def map_region_with_questionnaires(self):
        questionnaire_region_map = {}
        regional_questionnaires = self.questionnaires.filter(region__isnull=False)
        for region in self.regions:
            regional = {region: {'finalized': regional_questionnaires.filter(region=region, status=Questionnaire.FINALIZED),
                        'drafts': regional_questionnaires.filter(region=region, status=Questionnaire.DRAFT)}}
            questionnaire_region_map.update(regional)
        return questionnaire_region_map