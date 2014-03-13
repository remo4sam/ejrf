from questionnaire.features.pages.base import PageObject
from nose.tools import assert_equal


class ManageJrfPage(PageObject):
    url = "/manage/"

    def selectQuestionnaire(self, questionnaire):
        self.click_by_id('questionnaire-%s' % questionnaire.id)

    def validate_icon_present(self, _id, status=True):
        assert_equal(self.is_element_present_by_id(_id), status)


class AssignModal(PageObject):
    def validate_questions(self, *questions):
        self.is_element_present_by_css('modal-content')
        for question in questions:
            self.is_text_present(question.export_label)


class QuestionnairePreviewModal(PageObject):
    def validate_questions(self, *questions):
        self.is_element_present_by_css('modal-content')
        for question in questions:
            self.is_text_present(question.text)