from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from braces.views import MultiplePermissionsRequiredMixin, PermissionRequiredMixin
from questionnaire.forms.questionnaires import QuestionnaireFilterForm
from questionnaire.mixins import RegionAndPermissionRequiredMixin, OwnerAndPermissionRequiredMixin
from questionnaire.models import Questionnaire, Region

class ManageJRF(MultiplePermissionsRequiredMixin, View):
    permissions = {'any': ('auth.can_view_users',)}

    def __init__(self, *args, **kwargs):
        super(ManageJRF, self).__init__(**kwargs)
        self.template_name = 'home/global/index.html'
        self.questionnaires = Questionnaire.objects.all().order_by('-year')
        self.regions = Region.objects.filter(organization__name='WHO').order_by('name')

    def get(self, *args, **kwargs):
        core_questionnaires = self.questionnaires.filter(region__isnull=True)
        context = {'finalized_questionnaires': core_questionnaires.filter(status__in=[Questionnaire.FINALIZED, Questionnaire.PUBLISHED]),
                   'draft_questionnaires': core_questionnaires.filter(status=Questionnaire.DRAFT),
                   'filter_form': QuestionnaireFilterForm(),
                   'regions_questionnaire_map': self.map_region_with_questionnaires(),
                   'regions': self.regions,
                   'btn_label': 'Duplicate',
                   'action': reverse('duplicate_questionnaire_page')}
        return render(self.request, self.template_name, context)

    def map_region_with_questionnaires(self):
        questionnaire_region_map = {}
        regional_questionnaires = self.questionnaires.filter(region__isnull=False)
        for region in self.regions:
            regional = {region: {'finalized': regional_questionnaires.filter(region=region, status__in=[Questionnaire.FINALIZED, Questionnaire.PUBLISHED]),
                        'drafts': regional_questionnaires.filter(region=region, status=Questionnaire.DRAFT)}}
            questionnaire_region_map.update(regional)
        return questionnaire_region_map


class EditQuestionnaireNameView(PermissionRequiredMixin, View):
    permission_required = 'auth.can_edit_questionnaire'

    def post(self, *args, **kwargs):
        questionnaire = Questionnaire.objects.get(id=kwargs['questionnaire_id'])
        questionnaire.name = self.request.POST['name']
        questionnaire.save()
        message = "Name of Questionnaire updated successfully."
        messages.success(self.request, message)
        return HttpResponseRedirect(reverse('manage_jrf_page'))


class ManageRegionalJRF(RegionAndPermissionRequiredMixin, View):
    permission_required = 'auth.can_edit_questionnaire'

    def __init__(self, *args, **kwargs):
        super(ManageRegionalJRF, self).__init__(**kwargs)
        self.template_name = 'home/regional/index.html'

    def get(self, *args, **kwargs):
        region = Region.objects.get(id=kwargs['region_id'])
        questionnaires = region.questionnaire.all()
        context = {'region': region,
                   'finalized_questionnaires': questionnaires.filter(status__in=[Questionnaire.FINALIZED, Questionnaire.PUBLISHED]),
                   'draft_questionnaires': questionnaires.filter(status=Questionnaire.DRAFT),}
        return render(self.request, self.template_name, context)

