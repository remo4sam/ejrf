from braces.views import AccessMixin, MultiplePermissionsRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from questionnaire.models import Questionnaire, Region


class RegionAndPermissionRequiredMixin(AccessMixin):
    permission_required = None

    def dispatch(self, request, *args, **kwargs):
        if self.permission_required is None:
            raise ImproperlyConfigured(
                "'PermissionRequiredMixin' requires "
                "'permission_required' attribute to be set.")
        has_permission = self.get_permissions_from_request(request, **kwargs)

        if not has_permission:
            if self.raise_exception:
                raise PermissionDenied
            else:
                return redirect_to_login(request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())
        return super(RegionAndPermissionRequiredMixin, self).dispatch(request, *args, **kwargs)

    def get_permissions_from_request(self, request, **kwargs):
        user = request.user
        region = None
        if 'questionnaire_id' in kwargs:
            region = Questionnaire.objects.get(id=kwargs['questionnaire_id']).region
        if 'region_id' in kwargs:
            region = Region.objects.get(id=kwargs['region_id'])
        return user.has_perm(self.permission_required) and user.user_profile and user.user_profile.region == region


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
