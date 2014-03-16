from django.shortcuts import render
from django.views.generic import View
from braces.views import MultiplePermissionsRequiredMixin
from questionnaire.models import Questionnaire, Country
from questionnaire.services.users import UserQuestionnaireService


class PreviewQuestionnaire(MultiplePermissionsRequiredMixin, View):
    def __init__(self):
        super(PreviewQuestionnaire, self).__init__()
        self.template_name = "questionnaires/entry/preview.html"
        self.permissions = {"any": ("auth.can_submit_responses", "auth.can_view_questionnaire")}
        self.questionnaires = Questionnaire.objects.all()

    def get(self, request, *args, **kwargs):
        if 'questionnaire_id' in kwargs.keys():
            questionnaire = self.questionnaires.get(id=kwargs.get('questionnaire_id'))
        else:
            user_country = self.request.user.user_profile.country
            questionnaire = self.questionnaires.get(status=Questionnaire.PUBLISHED, region__countries=user_country)

        user_questionnaire_service = self.get_questionnaire_user_service(questionnaire)
        context = {'all_sections_questionnaires': user_questionnaire_service.all_sections_questionnaires(),
                   'ordered_sections': questionnaire.sections.order_by('order')}
        return render(request, self.template_name, context)

    def get_questionnaire_user_service(self, questionnaire):
        get_params = self.request.GET
        if 'country' in get_params and 'version' in get_params and 'region' in get_params:
            country = Country.objects.get(id=get_params['country'])
            questionnaire = self.questionnaires.get(status=Questionnaire.PUBLISHED, region_id=get_params['region'])
            return UserQuestionnaireService(country, questionnaire,  get_params['version'])
        return UserQuestionnaireService(self.request.user.user_profile.country, questionnaire)