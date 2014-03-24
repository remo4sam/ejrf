from braces.views import AccessMixin, MultiplePermissionsRequiredMixin
from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseRedirect
from questionnaire.models import Questionnaire, Region, SubSection, Question, Section


class RegionalPermissionRequired(AccessMixin):
    permission_required = None

    def dispatch(self, request, *args, **kwargs):
        has_permission = self.get_permissions_from_request(request, **kwargs)
        if not has_permission:
            return redirect_to_login(request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())
        return super(RegionalPermissionRequired, self).dispatch(request, *args, **kwargs)

    def get_permissions_from_request(self, request, **kwargs):
        user = request.user
        regions = self.get_region(kwargs)
        return user.has_perm(self.permission_required) and self._from_same_region(user, regions)

    def get_region(self, kwargs):
        pass

    def _from_same_region(self, user, regions):
        same_region_check = [user.user_profile.region == region for region in regions]
        return same_region_check.count(True) == len(regions)


class RegionAndPermissionRequiredMixin(RegionalPermissionRequired):

    def get_region(self, kwargs):
        if 'region_id' in kwargs:
            return [Region.objects.get(id=kwargs['region_id'])]
        regions = []
        if 'question_id' in kwargs:
            regions.append(Question.objects.get(id=kwargs['question_id']).region)
        if 'subsection_id' in kwargs:
            regions.append(SubSection.objects.get(id=kwargs['subsection_id']).section.questionnaire.region)
        if 'section_id' in kwargs:
            regions.append(Section.objects.get(id=kwargs['section_id']).questionnaire.region)
        if 'questionnaire_id' in kwargs:
            regions.append(Questionnaire.objects.get(id=kwargs['questionnaire_id']).region)
        return regions


class OwnerAndPermissionRequiredMixin(RegionalPermissionRequired):
    def get_region(self, kwargs):
        if 'subsection_id' in kwargs:
            return [SubSection.objects.get(id=kwargs['subsection_id']).region]
        object_ids = filter(lambda key: key.endswith('_id'), kwargs.keys())
        objects = [eval(object_id.replace("_id", "").capitalize()).objects.get(id=kwargs[object_id]) for object_id in object_ids]
        return [object.region for object in objects]


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