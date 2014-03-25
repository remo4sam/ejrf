from questionnaire.features.pages.base import PageObject


class QuestionListingPage(PageObject):
    url = "/questions/"

    def validate_question_attributes(self, question):
        self.browser.is_text_present(question.text)
        self.browser.is_text_present(question.export_label)
        self.browser.is_text_present(question.instructions)

        for option in question.options.all():
            self.browser.is_text_present(option.text)

class CreateQuestionPage(PageObject):
    url = "/questions/new/"

    def remove_option_field(self, selector, number):
        self.browser.find_by_css(selector)[number].click()

    def fill_first_visible_option(self, name, value):
        self.browser.find_by_name(name).last.fill(value)