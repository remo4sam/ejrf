from django.conf.urls import patterns, url
from questionnaire.views.assign_questions import AssignQuestion, UnAssignQuestion
from questionnaire.views.export_to_text import ExportToTextView, ExportSectionPDF, DownloadSectionPDF, SpecificExportView
from questionnaire.views.home import Home
from questionnaire.views.locations import ListRegions, ListCountries, RegionsForOrganization, CountriesForRegion
from questionnaire.views.manage import ManageJRF, ManageRegionalJRF, EditQuestionnaireNameView
from questionnaire.views.questionnaire_preview import PreviewQuestionnaire
from questionnaire.views.sections import NewSection, NewSubSection, EditSection, EditSubSection, DeleteSection, DeleteSubSection, \
    ReOrderQuestions
from questionnaire.views.questions import QuestionList, CreateQuestion, DeleteQuestion, EditQuestion
from questionnaire.views.questionnaires import Entry, SubmitQuestionnaire, DuplicateQuestionnaire, FinalizeQuestionnaire, UnfinalizeQuestionnaire, PublishQuestionnaire, ApproveQuestionnaire, DeleteAnswerRow
from questionnaire.views.theme import Theme, ThemeList, NewTheme, EditTheme, DeleteTheme
from questionnaire.views.upload_document import UploadDocument, DownloadDocument, DeleteDocument
from questionnaire.views.users import UsersList, CreateUser, EditUser

urlpatterns = patterns('',
    url(r'^$',  Home.as_view(), name="home_page"),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'users/login.html'}, name="login_page"),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/accounts/login/'}, name="logout_page"),
    url(r'^export-section/$', ExportSectionPDF.as_view(), name="questionnaire_export_page"),
    url(r'^export-section/(?P<filename>[\.\w]+)$', DownloadSectionPDF.as_view()),
    url(r'^extract/$', ExportToTextView.as_view(), name="export_page"),
    url(r'^extract/country/(?P<country_id>\d+)/version/(?P<version_number>\d+)/$', SpecificExportView.as_view(), name="specific_export_page"),
    url(r'^locations/region/$', ListRegions.as_view(), name='list_region_page'),
    url(r'^locations/countries/$', CountriesForRegion.as_view(), name="countries_for_region"),
    url(r'^locations/organization/(?P<organization_id>\d+)/region/$', RegionsForOrganization.as_view()),
    url(r'^locations/region/(?P<region_id>\d+)/country/$', ListCountries.as_view(), name="list_country_page"),
    url(r'^manage/$', ManageJRF.as_view(), name='manage_jrf_page'),
    url(r'^manage/questionnaire/(?P<questionnaire_id>\d+)/edit_name/$', EditQuestionnaireNameView.as_view(), name="edit_questionnaire_name"),
    url(r'^manage/region/(?P<region_id>\d+)/$', ManageRegionalJRF.as_view(), name='manage_regional_jrf_page'),
    url(r'^questionnaire/entry/(?P<questionnaire_id>\d+)/section/(?P<section_id>\d+)/$',Entry.as_view(), name="questionnaire_entry_page"),
    url(r'^questionnaire/entry/(?P<questionnaire_id>\d+)/section/(?P<section_id>\d+)/delete/(?P<group_id>\d+)/$', DeleteAnswerRow.as_view()),
    url(r'^questionnaire/entry/(?P<questionnaire_id>\d+)/section/new/$', NewSection.as_view(), name="new_section_page"),
    url(r'^questionnaire/entry/(?P<questionnaire_id>\d+)/section/(?P<section_id>\d+)/subsection/new/$', NewSubSection.as_view(), name="new_subsection_page"),
    url(r'^questionnaire/(?P<questionnaire_id>\d+)/approve/$', ApproveQuestionnaire.as_view(), name="approve_questionnaire_page"),
    url(r'^questionnaire/(?P<questionnaire_id>\d+)/finalize/$', FinalizeQuestionnaire.as_view(), name="finalize_questionnaire_page"),
    url(r'^questionnaire/(?P<questionnaire_id>\d+)/unfinalize/$', UnfinalizeQuestionnaire.as_view(), name="unfinalize_questionnaire_page"),
    url(r'^questionnaire/(?P<questionnaire_id>\d+)/publish/$', PublishQuestionnaire.as_view(), name="publish_questionnaire_page"),
    url(r'^questionnaire/(?P<questionnaire_id>\d+)/preview/$', PreviewQuestionnaire.as_view(), name="preview_specific_questionnaire"),
    url(r'^questionnaire/entry/(?P<questionnaire_id>\d+)/documents/upload/$', UploadDocument.as_view(), name='upload_document'),
    url(r'^questionnaire/entry/(?P<questionnaire_id>\d+)/documents/(?P<document_id>\d+)/download/$', DownloadDocument.as_view(), name='download_document'),
    url(r'^questionnaire/document/(?P<document_id>\d+)/delete/$', DeleteDocument.as_view(), name='delete_document'),
    url(r'^questionnaire/entry/duplicate/$',  DuplicateQuestionnaire.as_view(), name='duplicate_questionnaire_page'),
    url(r'^questions/$', QuestionList.as_view(), name='list_questions_page'),
    url(r'^questions/new/$', CreateQuestion.as_view(), name='new_question_page'),
    url(r'^questions/(?P<question_id>\d+)/edit/$', EditQuestion.as_view(), name='edit_question_page'),
    url(r'^questions/(?P<question_id>\d+)/delete/$', DeleteQuestion.as_view(), name='delete_question_page'),
    url(r'^submit/(?P<questionnaire_id>\d+)$', SubmitQuestionnaire.as_view(), name="submit_questionnaire_page"),
    url(r'^subsection/(?P<subsection_id>\d+)/assign_questions/$', AssignQuestion.as_view(), name="assign_question_to_subsection_page"),
    url(r'^subsection/(?P<subsection_id>\d+)/question/(?P<question_id>\d+)/unassign/$', UnAssignQuestion.as_view(), name="unassign_question_page"),
    url(r'^subsection/(?P<subsection_id>\d+)/reorder/$', ReOrderQuestions.as_view(), name="reorder_page"),
    url(r'^section/(?P<section_id>\d+)/edit/$', EditSection.as_view(), name="edit_section_page"),
    url(r'^section/(?P<section_id>\d+)/delete/', DeleteSection.as_view(), name="delete_section_page"),
    url(r'^subsection/(?P<subsection_id>\d+)/edit/$', EditSubSection.as_view(), name="edit_subsection_page"),
    url(r'^subsection/(?P<subsection_id>\d+)/delete/$', DeleteSubSection.as_view(), name="delete_subsection_page"),
    url(r'^themes/$', ThemeList.as_view(), name="theme_list_page"),
    url(r'^themes/(?P<theme_id>\d+)/edit/$', EditTheme.as_view(), name="edit_theme_page"),
    url(r'^themes/(?P<theme_id>\d+)/delete/$', DeleteTheme.as_view(), name="delete_theme_page"),
    url(r'^themes/new/$', NewTheme.as_view(), name="new_theme_page"),
    url(r'^users/$', UsersList.as_view(), name="list_users_page"),
    url(r'^users/new/$', CreateUser.as_view(), name="create_user_page"),
    url(r'^users/(?P<user_id>\d+)/edit/$', EditUser.as_view(), name="edit_user"),
)