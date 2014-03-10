from lettuce import world
from questionnaire.features.pages.base import PageObject
from questionnaire.features.pages.home import HomePage


class LoginPage(PageObject):
    url = "/accounts/login/"

    def login(self, user, password):
        details = {'username': user.username,
                   'password': password,}

        self.browser.fill_form(details)
        self.submit()

    def links_present_by_text(self, links_text):
        for text in links_text:
            assert self.browser.find_link_by_text(text)

class UserListingPage(PageObject):
    url = "/users/"

    def validate_user_list_headers(self):
        self.is_text_present("Username", "Email", "Roles", "Organization / Region / Country", "Status", "Actions")

    def validate_select_not_present(self, name):
        assert len(self.browser.find_option_by_text(name)) == 0


class CreateUserPage(PageObject):
    url = "/users/new/"

    def validate_only_organization_drop_down_visible(self):
        assert len(self.browser.find_by_id('organization')) == 1
        assert len(self.browser.find_by_id('region')) == 0
        assert len(self.browser.find_by_id('country')) == 0

    def validate_only_organization_and_region_drop_down_visible(self):
        assert len(self.browser.find_by_id('organization')) == 1
        assert len(self.browser.find_by_id('region')) == 1
        assert len(self.browser.find_by_id('country')) == 0

    def validate_only_country_drop_down_visible(self):
        assert len(self.browser.find_by_id('organization')) == 0
        assert len(self.browser.find_by_id('region')) == 0
        assert len(self.browser.find_by_id('country')) == 1