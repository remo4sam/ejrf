from questionnaire.features.pages.base import PageObject


class ManageJrfPage(PageObject):
    url = "/manage/"

    def selectQuestionnaire(self, questionnaire):
        self.click_by_id('questionnaire-%s' % questionnaire.id)


class AssignModal(PageObject):
    def validate_questions(self, *questions):
        self.is_element_present_by_css('modal-content')
        for question in questions:
            self.is_text_present(question.export_label)