from braces.views import AccessMixin
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from questionnaire.models import Questionnaire


class RegionAndPermissionRequiredMixin(AccessMixin):
    permission_required = None

    def dispatch(self, request, *args, **kwargs):
        if self.permission_required is None:
            raise ImproperlyConfigured(
                "'PermissionRequiredMixin' requires "
                "'permission_required' attribute to be set.")
        user = request.user
        questionnaire = Questionnaire.objects.get(id=kwargs['questionnaire_id'])
        has_permission = user.has_perm(self.permission_required) and user.user_profile and user.user_profile.region == questionnaire.region


        if not has_permission:
            if self.raise_exception:
                raise PermissionDenied
            else:
                return redirect_to_login(request.get_full_path(),
                                         self.get_login_url(),
                                         self.get_redirect_field_name())

        return super(RegionAndPermissionRequiredMixin, self).dispatch(request, *args, **kwargs)
