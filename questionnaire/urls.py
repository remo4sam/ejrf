from django.conf.urls import patterns, url
from questionnaire.views.assign_questions import AssignQuestion, UnAssignQuestion
from questionnaire.views.export_to_text import ExportToTextView, ExportSectionPDF, DownloadSectionPDF
from questionnaire.views.home import Home
from questionnaire.views.locations import ListRegions, ListCountries, RegionsForOrganization
from questionnaire.views.manage import ManageJRF
from questionnaire.views.questionnaire_preview import PreviewQuestionnaire
from questionnaire.views.sections import NewSection, NewSubSection, EditSection, EditSubSection
from questionnaire.views.questions import QuestionList, CreateQuestion, DeleteQuestion
from questionnaire.views.questionnaires import Entry, SubmitQuestionnaire, DuplicateQuestionnaire
from questionnaire.views.upload_document import UploadDocument, DownloadDocument, DeleteDocument
from questionnaire.views.users import UsersList, CreateUser, EditUser

urlpatterns = patterns('',
    url(r'^$',  Home.as_view(), name="home_page"),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'users/login.html'}, name="login_page"),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/accounts/login/'}, name="logout_page"),
    url(r'^export-section/$', ExportSectionPDF.as_view(), name="questionnaire_export_page"),
    url(r'^export-section/(?P<filename>[\.\w]+)$', DownloadSectionPDF.as_view()),
    url(r'^extract/$', ExportToTextView.as_view(), name="export_page"),
    url(r'^locations/region/$', ListRegions.as_view(), name='list_region_page'),
    url(r'^locations/organization/(?P<organization_id>\d+)/region/$', RegionsForOrganization.as_view()),
    url(r'^locations/region/(?P<region_id>\d+)/country/$', ListCountries.as_view(), name="list_country_page"),
    url(r'^manage/$', ManageJRF.as_view(), name='manage_jrf_page'),
    url(r'^questionnaire/entry/(?P<questionnaire_id>\d+)/section/(?P<section_id>\d+)/$',
        Entry.as_view(), name="questionnaire_entry_page"),
    url(r'^questionnaire/entry/(?P<questionnaire_id>\d+)/section/new/$', NewSection.as_view(), name="new_section_page"),
    url(r'^questionnaire/entry/(?P<questionnaire_id>\d+)/section/(?P<section_id>\d+)/subsection/new/$',
        NewSubSection.as_view(), name="new_subsection_page"),
    url(r'^questionnaire/preview/$', PreviewQuestionnaire.as_view(),
        name="preview_questionnaire"),
    url(r'^questionnaire/preview/(?P<questionnaire_id>\d+)$', PreviewQuestionnaire.as_view(),
        name="preview_specific_questionnaire"),
    url(r'^questionnaire/documents/upload/$', UploadDocument.as_view(), name='upload_document'),
    url(r'^questionnaire/entry/(?P<questionnaire_id>\d+)/documents/(?P<document_id>\d+)/download/$',
        DownloadDocument.as_view(), name='download_document'),
    url(r'^questionnaire/document/(?P<document_id>\d+)/delete/$',
        DeleteDocument.as_view(), name='delete_document'),
    url(r'^questionnaire/entry/duplicate/$',  DuplicateQuestionnaire.as_view(), name='duplicate_questionnaire_page'),
    url(r'^questions/$', QuestionList.as_view(), name='list_questions_page'),
    url(r'^questions/new/$', CreateQuestion.as_view(), name='new_question_page'),
    url(r'^questions/(?P<question_id>\d+)/delete/$', DeleteQuestion.as_view(), name='delete_question_page'),
    url(r'^submit/$', SubmitQuestionnaire.as_view(), name="submit_questionnaire_page"),
    url(r'^subsection/(?P<subsection_id>\d+)/assign_questions/$', AssignQuestion.as_view(), name="assign_question_to_subsection_page"),
    url(r'^subsection/(?P<subsection_id>\d+)/question/(?P<question_id>\d+)/unassign/$', UnAssignQuestion.as_view(), name="unassign_question_page"),
    url(r'^section/(?P<section_id>\d+)/edit/$', EditSection.as_view(), name="edit_section_page"),
    url(r'^subsection/(?P<subsection_id>\d+)/edit/$', EditSubSection.as_view(), name="edit_subsection_page"),
    url(r'^users/$', UsersList.as_view(), name="list_users_page"),
    url(r'^users/new/$', CreateUser.as_view(), name="create_user_page"),
    url(r'^users/(?P<pk>\d+)/edit/$', EditUser.as_view(), name="edit_user"),
)