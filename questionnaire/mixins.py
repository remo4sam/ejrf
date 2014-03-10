from braces.views import AccessMixin, MultiplePermissionsRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from questionnaire.models import Questionnaire, Region, SubSection


class RegionAndPermissionRequiredMixin(AccessMixin):
    permission_required = None

    def dispatch(self, request, *args, **kwargs):
        has_permission = self.get_permissions_from_request(request, **kwargs)
        if not has_permission:
            return redirect_to_login(request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())
        return super(RegionAndPermissionRequiredMixin, self).dispatch(request, *args, **kwargs)

    def get_permissions_from_request(self, request, **kwargs):
        user = request.user
        region = self.get_region(kwargs)
        return user.has_perm(self.permission_required) and user.user_profile and user.user_profile.region == region

    def get_region(self, kwargs):
        if 'questionnaire_id' in kwargs:
            return Questionnaire.objects.get(id=kwargs['questionnaire_id']).region
        if 'region_id' in kwargs:
            return Region.objects.get(id=kwargs['region_id'])
        if 'subsection_id' in kwargs:
            subsection = SubSection.objects.get(id=kwargs['subsection_id'])
            return subsection.region or subsection.section.region or subsection.section.questionnaire.region
        return None


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
