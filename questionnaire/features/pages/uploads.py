import re
from questionnaire.features.pages.base import PageObject


class UploadDocumentPage(PageObject):
    def __init__(self, browser, questionnaire):
        super(UploadDocumentPage, self).__init__(browser)
        self.questionnaire = questionnaire
        self.url = '/questionnaire/entry/%d/documents/upload/' % questionnaire.id

    def validate_upload_form(self, data):
        for label, field in data.items():
            self.is_text_present(label)
            assert self.browser.find_by_name(field)

    def validate_number_of_attachments(self, expected_number_of_attachments):
        label = self.browser.find_by_css('a.attachement').text
        number_of_attachments_shown_in_label = 0

        number_found_in_label = re.findall('\d+', label)
        if number_found_in_label:
            number_of_attachments_shown_in_label = int(number_found_in_label[0])
        assert (number_of_attachments_shown_in_label == expected_number_of_attachments)


class DeleteDocumentPage(PageObject):
    def __init__(self, browser, document):
        super(DeleteDocumentPage, self).__init__(browser)
        self.url = '/questionnaire/document/%s/delete/' % document.id