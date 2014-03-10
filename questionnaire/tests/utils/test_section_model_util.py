from questionnaire.models import Questionnaire, Section, SubSection
from questionnaire.tests.base_test import BaseTest
from questionnaire.utils.model_utils import reindex_orders_in


class SectionUtilTest(BaseTest):
    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013,
                                                          status=Questionnaire.FINALIZED)
        self.section_1 = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)",
                                                order=1, questionnaire=self.questionnaire, name="Reported Cases")
        self.section_2 = Section.objects.create(title="Cured Cases of Measles 1", order=2,
                                                questionnaire=self.questionnaire, name="Cured Cases")
        self.section_3 = Section.objects.create(title="Cured Cases of Measles 2", order=3,
                                                questionnaire=self.questionnaire, name="Cured Cases")
        self.section_4 = Section.objects.create(title="Cured Cases of Measles 3", order=4,
                                                questionnaire=self.questionnaire, name="Cured Cases")

        self.sub_section1 = SubSection.objects.create(title="Cured Cases of Measles 3", order=1, section=self.section_1)
        self.sub_section2 = SubSection.objects.create(title="Cured Cases of Measles 3", order=2, section=self.section_1)
        self.sub_section3 = SubSection.objects.create(title="Cured Cases of Measles 3", order=3, section=self.section_1)

    def test_re_indexes_section_orders_after_deletion_of_section(self):
        Section.objects.get(id=self.section_3.id).delete()

        reindex_orders_in(Section, questionnaire=self.questionnaire)

        self.assertEqual([1, 2, 3], list(Section.objects.values_list('order', flat=True)))

    def test_re_indexes_section_orders_after_deletion_of_subsection(self):
        SubSection.objects.get(id=self.sub_section2.id).delete()

        reindex_orders_in(SubSection, section=self.section_1)

        self.assertEqual([1, 2], list(SubSection.objects.values_list('order', flat=True)))