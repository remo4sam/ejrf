from lettuce.django import django_url
from nose.tools import assert_equals


class PageObject(object):
    url = None

    def __init__(self, browser):
        self.browser = browser

    def visit(self):
        self.browser.visit(django_url(self.url))

    def validate_url(self):
        assert self.browser.url == django_url(self.url)

    def fill(self, name, value):
        self.browser.fill(name, value)

    def submit(self):
        self.browser.find_by_css("form button").first.click()

    def click_link_by_text(self, text):
        self.browser.click_link_by_text(text)

    def click_by_css(self, css_selector):
        self.browser.find_by_css(css_selector).first.click()

    def click_link_by_partial_href(self, modal_id):
        self.browser.click_link_by_partial_href(modal_id)

    def click_link_by_href(self, modal_id):
        self.browser.click_link_by_href(modal_id)

    def click_by_name(self, name):
        self.browser.find_by_name(name).first.click()

    def _is_text_present(self, text, status=True):
        assert_equals(status, self.browser.is_text_present(text))

    def is_text_present(self, *texts, **kwargs):
        status = kwargs['status'] if 'status' in kwargs else True
        for text in texts:
            self._is_text_present(text, status)

    def validate_pagination(self):
        self.click_link_by_text('2')

    def fill_form(self, data):
        self.browser.fill_form(data)

    def fill_this_form(self, form_css, data):
        for name, value in data.items():
            the_form_element = self.browser.find_by_css('%s #id_%s' % (form_css, name))
            the_form_element.fill(value)

    def click_by_id(self, id):
        self.browser.find_by_id(id).first.click()

    def number_of_elements(self, element_name):
        return len(self.browser.find_by_name(element_name))

    def check(self, value):
        self.browser.find_by_value(value).first.check()

    def uncheck_by_name(self, value):
        self.browser.find_by_name(value).first.uncheck()

    def select(self, name, value):
        self.browser.select(name, value)

    def is_element_present_by_css(self, css_selector):
        self.browser.is_element_present_by_css(css_selector)

    def input_file(self, filename):
        self.browser.attach_file('path', filename)

    def is_element_present_by_value(self, value):
        self.browser.is_element_present_by_value(value)

    def is_element_present_by_id(self, element_id):
        self.browser.is_element_present_by_id(element_id)

    def confirm_delete(self, model):
        self.is_text_present("Confirm Delete", "Are you sure you want to delete this %s?" % model)

    def is_text_not_present(self, text):
        self.browser.is_text_not_present(text)