from django.shortcuts import render
from django.views.generic import View
from braces.views import MultiplePermissionsRequiredMixin
from questionnaire.models import Questionnaire, Country
from questionnaire.services.users import UserQuestionnaireService


class PreviewQuestionnaire(MultiplePermissionsRequiredMixin, View):
    def __init__(self):
        super(PreviewQuestionnaire, self).__init__()
        self.template_name = "questionnaires/entry/preview.html"
        self.permissions = {"any": ("auth.can_submit_responses", "auth.can_view_questionnaire", 'auth.can_view_users')}
        self.questionnaires = Questionnaire.objects.all()

    def get(self, request, *args, **kwargs):
        questionnaire_id = kwargs.get('questionnaire_id')
        questionnaire = self.questionnaires.get(id=questionnaire_id)
        if self.request.user.has_perm('auth.can_submit_responses'):
            user_country = self.request.user.user_profile.country
            questionnaire = self.questionnaires.get(id=questionnaire_id, region__countries=user_country)

        user_questionnaire_service = self.get_questionnaire_user_service(questionnaire)
        context = {'all_sections_questionnaires': user_questionnaire_service.all_sections_questionnaires(),
                   'ordered_sections': questionnaire.sections.order_by('order') if questionnaire else None,
                   'questionnaire': questionnaire,
                   'documents': user_questionnaire_service.attachments()}

        return render(request, self.template_name, context)

    def get_questionnaire_user_service(self, questionnaire):
        get_params = self.request.GET
        if 'country' in get_params and 'version'in get_params:
            country = Country.objects.get(id=get_params['country'])
            return UserQuestionnaireService(country, questionnaire,  get_params['version'])
        return UserQuestionnaireService(self.request.user.user_profile.country, questionnaire)