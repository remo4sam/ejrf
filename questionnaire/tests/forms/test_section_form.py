from questionnaire.forms.sections import SectionForm, SubSectionForm
from questionnaire.models import Questionnaire, Section, SubSection
from questionnaire.tests.base_test import BaseTest


class CoreSectionFormTest(BaseTest):

    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013)
        self.form_data = {'name': 'New section',
                          'description': 'funny section',
                          'title': 'some title',
                          'questionnaire': self.questionnaire.id}

    def test_valid(self):
        section_form = SectionForm(initial={'questionnaire': self.questionnaire.id}, data=self.form_data)
        self.assertTrue(section_form.is_valid())

    def test_valid_with_initial(self):
        section_form = SectionForm(data=self.form_data, initial={'questionnaire': self.questionnaire.id})
        self.assertTrue(section_form.is_valid())


class CoreSubSectionFormTest(BaseTest):

    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013)
        self.section = Section.objects.create(name="section", questionnaire=self.questionnaire, order=1)
        self.form_data = {'description': 'funny subsection',
                          'title': 'some subsection'}

    def test_valid(self):
        subsection_form = SubSectionForm(initial={'section': self.section.id}, data=self.form_data)
        self.assertTrue(subsection_form.is_valid())

    def test_empty_title_is_valid(self):
        data = self.form_data.copy()
        data['title'] = ''

        subsection_form = SubSectionForm(initial={'section': self.section.id}, data=data)

        self.assertTrue(subsection_form.is_valid())

    def test_empty_description_is_invalid(self):
        data = self.form_data.copy()
        data['description'] = ''

        subsection_form = SubSectionForm(initial={'section': self.section.id}, data=data)

        self.assertTrue(subsection_form.is_valid())

    def test_save_increment_order(self):
        existing_subs = SubSection.objects.create(title="subsection 1", section=self.section, order=1)
        data = self.form_data.copy()

        subsection_form = SubSectionForm(instance=SubSection(section=self.section), data=data)
        subsection_form.save()
        new_subs = SubSection.objects.filter(section=self.section, **data)
        self.failUnless(new_subs)
        self.assertEqual(1, new_subs.count())
        self.assertEqual(existing_subs.order + 1, new_subs[0].order)

    def test_save_does_not_increment_order_if_instance_of_section_is_given_and_it_has_order(self):
        subsection_order = 1
        existing_subs = SubSection.objects.create(title="subsection 1", section=self.section, order=subsection_order)
        data = self.form_data.copy()

        subsection_form = SubSectionForm(instance=existing_subs, data=data)
        subsection_form.save()
        new_subs = SubSection.objects.filter(section=self.section, **data)
        self.failUnless(new_subs)
        self.assertEqual(1, new_subs.count())
        self.assertEqual(subsection_order, new_subs[0].order)