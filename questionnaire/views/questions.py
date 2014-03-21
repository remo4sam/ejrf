from braces.views import PermissionRequiredMixin
from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView, DeleteView, View, UpdateView
from questionnaire.forms.questions import QuestionForm
from questionnaire.mixins import DoesNotExistExceptionHandlerMixin, OwnerAndPermissionRequiredMixin
from questionnaire.models import Question, Questionnaire


class QuestionList(PermissionRequiredMixin, View):
    permission_required = 'auth.can_edit_questionnaire'
    template_name = 'questions/index.html'
    model = Question

    def get(self, *args, **kwargs):
        finalized_questionnaire = Questionnaire.objects.filter(status=Questionnaire.FINALIZED)
        active_questions = None
        if finalized_questionnaire.exists():
            active_questions = finalized_questionnaire.latest('created').get_all_questions()
        questions = self.get_questions_for_user().filter(child=None)
        context = {'request': self.request,
                   'questions': questions,
                   'active_questions': active_questions}
        return render(self.request, self.template_name, context)

    def get_questions_for_user(self):
        if self.request.user.has_perm('auth.can_view_users'):
            return self.model.objects.filter(region=None).order_by('created')
        return self.model.objects.filter(region=self.request.user.user_profile.region)


class CreateQuestion(PermissionRequiredMixin, CreateView):
    permission_required = 'auth.can_edit_questionnaire'

    def __init__(self, **kwargs):
        super(CreateQuestion, self).__init__(**kwargs)
        self.template_name = 'questions/new.html'
        self.object = Question
        self.model = Question
        self.form_class = QuestionForm
        self.form = None

    def get_context_data(self, **kwargs):
        context = super(CreateQuestion, self).get_context_data(**kwargs)
        context.update({'btn_label': 'CREATE', 'id': 'id-new-question-form',
                        'cancel_url': reverse('list_questions_page'), 'title': 'New Question'})
        return context

    def post(self, request, *args, **kwargs):
        region = self.request.user.user_profile.region
        self.form = QuestionForm(region=region, data=request.POST)
        if self.form.is_valid():
            return self._form_valid()
        return self._form_invalid()

    def _form_valid(self):
        self.form.save()
        messages.success(self.request, "Question successfully created.")
        return HttpResponseRedirect(reverse('list_questions_page'))

    def _form_invalid(self):
        messages.error(self.request, "Question NOT created. See errors below.")
        context = {'form': self.form, 'btn_label': "CREATE", 'id': 'id-new-question-form',
                   'cancel_url': reverse('list_questions_page'), 'title': 'New Question'}
        return self.render_to_response(context)


class EditQuestion(PermissionRequiredMixin, UpdateView):
    permission_required = 'auth.can_edit_questionnaire'

    def __init__(self, **kwargs):
        super(EditQuestion, self).__init__(**kwargs)
        self.template_name = 'questions/new.html'
        self.model = Question
        self.form_class = QuestionForm
        self.success_url = reverse('list_questions_page')
        self.pk_url_kwarg = 'question_id'

    def get_context_data(self, **kwargs):
        context = super(EditQuestion, self).get_context_data(**kwargs)
        context.update({'btn_label': 'SAVE', 'id': 'id-new-question-form',
                        'cancel_url': reverse('list_questions_page'),
                        'title': 'Edit Question'})
        return context

    def form_valid(self, form):
        message = "Question successfully updated."
        messages.success(self.request, message)
        return super(EditQuestion, self).form_valid(form)

    def form_invalid(self, form):
        message = "Question NOT updated. See errors below."
        messages.error(self.request, message)
        return super(EditQuestion, self).form_invalid(form)


class DeleteQuestion(DoesNotExistExceptionHandlerMixin, OwnerAndPermissionRequiredMixin, DeleteView):
    def __init__(self, *args, **kwargs):
        super(DeleteQuestion, self).__init__(*args, **kwargs)
        self.permission_required = 'auth.can_edit_questionnaire'
        self.pk_url_kwarg = 'question_id'
        self.success_url = reverse("home_page")
        self.model = Question
        self.does_not_exist_url = reverse_lazy('list_questions_page')
        self.error_message = "Sorry, You tried to delete a question does not exist."

    def post(self, *args, **kwargs):
        question = self.model.objects.get(pk=kwargs['question_id'])
        if question.can_be_deleted():
            question.delete()
            return self.redirect_and_render_success_message()
        return self.redirect_and_render_error_message()

    def redirect_and_render_error_message(self, message=None):
        message = "Question was not deleted because it has responses"
        messages.error(self.request, message)
        return HttpResponseRedirect(self.does_not_exist_url)

    def redirect_and_render_success_message(self):
        message = "Question was deleted successfully"
        messages.success(self.request, message)
        return HttpResponseRedirect(self.does_not_exist_url)