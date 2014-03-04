from braces.views import PermissionRequiredMixin
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView
from questionnaire.forms.filter import UserFilterForm
from questionnaire.forms.user_profile import UserProfileForm, EditUserProfileForm
from questionnaire.models import Organization, Region, Country


class UsersList(PermissionRequiredMixin, ListView):
    permission_required = 'auth.can_view_users'

    FORM_QUERY_FIELD = {'role': 'groups',
                        'organization': 'user_profile__organization',
                        'region': 'user_profile__region'}

    COUNTRY_QUERY_FIELD = {'role': 'groups',
                           'organization': 'user_profile__country__regions__organization',
                           'region': 'user_profile__country__regions'}

    def __init__(self, **kwargs):
        super(UsersList, self).__init__(**kwargs)
        self.template_name = 'users/index.html'
        self.model = User
        self.object_list = self.get_queryset()

    def get(self, *args, **kwargs):
        context = {'request': self.request, 'users': self.object_list, 'filter_form': UserFilterForm()}
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = UserFilterForm(request.POST)
        if form.is_valid():
            global_query_params = self._query_for(request.POST.iteritems(), self.FORM_QUERY_FIELD)
            regional_query_params = self._query_for(request.POST.iteritems(), self.COUNTRY_QUERY_FIELD)
            filtered_users = self.object_list.filter(Q(**regional_query_params) | Q(**global_query_params))
            context = {'request': self.request,
                       'users': filtered_users,
                       'filter_form': form}
            return self.render_to_response(context)

    def _query_for(self, post, query_key_map):
        query_params = dict((self._get_query_field(key, query_key_map), value) for key, value in post if value.strip() != '' and key in query_key_map.keys())
        return query_params

    @staticmethod
    def _get_query_field(_key, query_key_map):
        return query_key_map.get(_key)

    def get_queryset(self):
        return self.model.objects.order_by('user_profile__created')


class CreateUser(PermissionRequiredMixin, CreateView):
    permission_required = 'auth.can_view_users'

    def __init__(self, **kwargs):
        super(CreateUser, self).__init__(**kwargs)
        self.form_class = UserProfileForm
        self.object = User
        self.template_name = "users/new.html"
        self.success_url = reverse('list_users_page')

    def form_valid(self, form):
        messages.success(self.request, "%s created successfully." % form.cleaned_data['groups'])
        return super(CreateUser, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateUser, self).get_context_data(**kwargs)
        context_vars = {'btn_label': "CREATE",
                        'title': "Create new user",
                        'organizations': Organization.objects.all(),
                        'regions': Region.objects.all(),
                        'countries': Country.objects.all()}
        context.update(context_vars)
        return context


class EditUser(PermissionRequiredMixin, UpdateView):
    permission_required = 'auth.can_view_users'

    def __init__(self, **kwargs):
        super(EditUser, self).__init__(**kwargs)
        self.template_name = 'users/new.html'
        self.object = User
        self.form_class = EditUserProfileForm
        self.success_url = reverse('list_users_page')

    def get(self, *args, **kwargs):
        user = User.objects.get(id=kwargs['pk'])
        context = {'btn_label': "SAVE",
                   'title': "Edit User",
                   'request': self.request,
                   'form': EditUserProfileForm(instance=user),
                   'cancel_url': reverse("list_users_page")}
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=kwargs['pk'])
        self.form =  EditUserProfileForm(instance=user, data=request.POST)
        if self.form.is_valid():
            return self._form_valid()
        return self._form_invalid()

    def _form_valid(self):
        self.form.save()
        message = "%s was successfully updated" % self.form.cleaned_data['username']
        messages.success(self.request, message)
        return HttpResponseRedirect(reverse("list_users_page"))

    def _form_invalid(self):
        message = "User was not updated, see errors below"
        messages.error(self.request, message )
        context = {'btn_label': "SAVE",
                   'title': "Edit User",
                   'request': self.request,
                   'form': self.form}
        return self.render_to_response(context)