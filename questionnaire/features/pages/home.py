from questionnaire.features.pages.base import PageObject


class HomePage(PageObject):
    url = "/"

    def links_present_by_text(self, links_text):
        for text in links_text:
            assert self.browser.find_link_by_text(text)

    def validate_extract_and_preview_versions(self, country):
        assert self.browser.is_element_present_by_id('view-country-%s-version-1' % country.id)
        assert self.browser.is_element_present_by_id('extract-country-%s-version-1' % country.id)
        assert self.browser.is_element_present_by_id('view-country-%s-version-2' % country.id)
        assert self.browser.is_element_present_by_id('extract-country-%s-version-2' % country.id)

    def validate_questionnaire_type_appears_in_right_category(self, questionnaire, type):
        if type == 'draft':
            assert self.browser.is_element_present_by_id('draft-questionnaire-%s' % questionnaire.id)
        if type == 'submitted':
            assert self.browser.is_element_present_by_id('submitted-questionnaire-%s' % questionnaire.id)
        if type == 'new':
            assert self.browser.is_element_present_by_id('new-questionnaire-%s' % questionnaire.id)
            
    def validate_questionnaire_opens_in_correct_mode(self, questionnaire, mode):
        assert self.browser.is_element_present_by_id('save_draft_button')
        assert self.browser.is_element_present_by_id('cancel_button')
        if mode == 'edit mode':
            assert self.browser.is_element_present_by_id('submit_questionnaire_btn')
        else:
            assert self.browser.is_element_present_by_id('edit_questionnaire_link')