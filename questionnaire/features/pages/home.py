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