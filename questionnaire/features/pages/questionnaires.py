from time import sleep
from questionnaire.features.pages.base import PageObject
from nose.tools import assert_true


class QuestionnairePage(PageObject):
    def __init__(self, browser, section):
        super(QuestionnairePage, self).__init__(browser)
        self.questionnaire = section.questionnaire
        self.section = section
        self.url = "/questionnaire/entry/%s/section/%s/" % (self.questionnaire.id, self.section.id)

    def validate_fields(self):
        assert self.browser.find_by_name("Number-0-response")
        assert self.browser.find_by_name("Number-1-response")
        assert self.browser.find_by_name("MultiChoice-0-response")
        assert self.browser.is_element_present_by_id('cancel_button')
        assert self.browser.is_element_present_by_id('save_draft_button')
        assert self.browser.is_element_present_by_id('submit_questionnaire_btn')

    def validate_instructions(self, question):
        self.click_by_css("#question-%d-instructions" % question.id)
        self.is_text_present(question.instructions)

    def validate_alert_success(self):
        self.is_text_present("Draft saved.")
        self.is_element_present_by_css(".alert-success")

    def validate_alert_error(self):
        self.is_text_present("Draft NOT saved. See errors below")
        self.is_element_present_by_css(".alert-danger")

    def validate_responses(self, data):
        data_keys = data.keys()
        numerical = filter(lambda key_: 'Number' in key_, data_keys)
        text = filter(lambda key_: 'Text' in key_, data_keys)
        for key in numerical:
            assert_true(self.browser.find_by_name(key).first.value in data.values())
        for key in text:
            assert_true(self.browser.find_by_name(key).first.value in data.values())

    def hover(self, name):
        self.browser.find_by_name(name).mouse_over()

    def validate_fields_disabled(self, data):
        for key in data:
            self.is_element_with_id_disabled('id_%s' % key)

    def validate_fields_enabled(self, data):
        for key in data:
            self.is_element_with_id_enabled('id_%s' % key)

    def validate_add_new_section_exists(self):
        self._is_text_present('New Section')
        assert self.is_element_present_by_id('new-section')