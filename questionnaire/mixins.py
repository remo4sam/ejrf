from braces.views import AccessMixin, MultiplePermissionsRequiredMixin
from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.http import HttpResponseRedirect
from questionnaire.models import Questionnaire, Region, SubSection, Question


class RegionAndPermissionRequiredMixin(AccessMixin):
    permission_required = None

    def dispatch(self, request, *args, **kwargs):
        has_permission = self.get_permissions_from_request(request, **kwargs)
        if not has_permission:
            return redirect_to_login(request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())
        return super(RegionAndPermissionRequiredMixin, self).dispatch(request, *args, **kwargs)

    def get_permissions_from_request(self, request, **kwargs):
        user = request.user
        regions = self.get_region(kwargs)
        return user.has_perm(self.permission_required) and self._from_same_region(user, regions)

    def get_region(self, kwargs):
        regions = []
        if 'question_id' in kwargs:
            question = Question.objects.get(id=kwargs['question_id'])
            regions.append(question.region)
        if 'subsection_id' in kwargs:
            subsection = SubSection.objects.get(id=kwargs['subsection_id'])
            regions.append(subsection.region or subsection.section.region or subsection.section.questionnaire.region)
        if 'questionnaire_id' in kwargs:
            regions.append(Questionnaire.objects.get(id=kwargs['questionnaire_id']).region)
        if 'region_id' in kwargs:
            regions.append(Region.objects.get(id=kwargs['region_id']))
        return regions

    def _from_same_region(self, user, regions):
        same_region_check = [user.user_profile.region == region for region in regions]
        return same_region_check.count(True) == len(regions)


class AdvancedMultiplePermissionsRequiredMixin(MultiplePermissionsRequiredMixin):
    permissions = None
    GET_permissions = None
    POST_permissions = None

    def _assign_permissions(self, request):
        self.permissions = self.GET_permissions or self.permissions
        if request.method == 'POST' and self.POST_permissions:
            self.permissions = self.POST_permissions

    def dispatch(self, request, *args, **kwargs):
        self._assign_permissions(request)
        return super(AdvancedMultiplePermissionsRequiredMixin, self).dispatch(request, *args, **kwargs)


class DoesNotExistExceptionHandlerMixin(AccessMixin):
    error_message = ""
    response = None
    model = None
    does_not_exist_url = ''

    def dispatch(self, request, *args, **kwargs):
        try:
            response = super(DoesNotExistExceptionHandlerMixin, self).dispatch(request, *args, **kwargs)
        except self.model.DoesNotExist:
            messages.error(request, self.error_message)
            return HttpResponseRedirect(self.does_not_exist_url)
        return response