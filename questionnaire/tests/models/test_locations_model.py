from questionnaire.models import Questionnaire, Section, QuestionGroup, Question, SubSection, Answer, MultiChoiceAnswer, NumericalAnswer
from questionnaire.models.answers import AnswerStatus, TextAnswer
from questionnaire.models.locations import Region, Country, Organization
from questionnaire.tests.base_test import BaseTest


class RegionTest(BaseTest):

    def test_region_fields(self):
        region = Region()
        fields = [str(item.attname) for item in region._meta.fields]
        self.assertEqual(6, len(fields))
        for field in ['id', 'created', 'modified', 'name', 'description', 'organization_id']:
            self.assertIn(field, fields)

    def test_store(self):
        org = Organization.objects.create(name="WHO")
        region = Region.objects.create(name="Region", organization=org)
        self.failUnless(region.id)
        self.assertEqual(org, region.organization)
        self.assertIsNone(region.description)


class CountryTest(BaseTest):
    def setUp(self):
        self.organisation = Organization.objects.create(name="WHO")
        self.afro = Region.objects.create(name="Afro", organization=self.organisation)
        self.uganda = Country.objects.create(name="Uganda", code="UGX")
        self.afro.countries.add(self.uganda)
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013, region=self.afro, status=Questionnaire.PUBLISHED)
        section_1 = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)", order=1,
                                           questionnaire=self.questionnaire, name="Reported Cases")
        sub_section = SubSection.objects.create(title="Reported cases for the year 2013", order=1, section=section_1)
        self.question2 = Question.objects.create(text='C. Number of cases positive', UID='C00005', answer_type='Number')

        self.parent = QuestionGroup.objects.create(subsection=sub_section, order=1)
        self.parent.question.add(self.question2)

    def test_country_fields(self):
        country = Country()
        fields = [str(item.attname) for item in country._meta.fields]
        self.assertEqual(5, len(fields))
        for field in ['id', 'created', 'modified', 'name', 'code']:
            self.assertIn(field, fields)

    def test_store(self):
        paho = Region.objects.create(name="PAHO")
        country = Country.objects.create(name="Peru")
        country.regions.add(paho)
        self.failUnless(country.id)
        regions = country.regions.all()
        self.assertEqual(1, regions.count())
        self.assertIn(paho, regions)

    def test_country_knows_answer_status_given_questionnaire(self):
        self.assertEqual(AnswerStatus.options[None], self.uganda.answer_status())
        answer = NumericalAnswer.objects.create(question=self.question2, country=self.uganda, status=Answer.DRAFT_STATUS,
                                                response=22)
        self.assertEqual(AnswerStatus.options['Draft'], self.uganda.answer_status())

        answer.status = Answer.SUBMITTED_STATUS
        answer.save()
        self.assertEqual(AnswerStatus.options[Answer.SUBMITTED_STATUS], self.uganda.answer_status())

    def test_country_gets_own_versions(self):
        NumericalAnswer.objects.create(question=self.question2, country=self.uganda, status=Answer.DRAFT_STATUS,
                                       response=22)
        self.assertEqual([1], self.uganda.all_versions())
        NumericalAnswer.objects.create(question=self.question2, country=self.uganda, status=Answer.DRAFT_STATUS,
                                       response=22, version=2)
        self.assertEqual([1, 2], self.uganda.all_versions())

    def test_country_gets_own_versions_given_a_questionnaire(self):
        NumericalAnswer.objects.create(question=self.question2, country=self.uganda, status=Answer.DRAFT_STATUS,
                                       response=22)
        self.assertEqual({self.questionnaire: [1]}, self.uganda.all_versions(self.questionnaire))
        NumericalAnswer.objects.create(question=self.question2, country=self.uganda, status=Answer.DRAFT_STATUS,
                                       response=22, version=2)
        self.assertEqual({self.questionnaire: [1, 2]}, self.uganda.all_versions(self.questionnaire))
        questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013, region=self.afro)
        self.assertEqual({questionnaire: []}, self.uganda.all_versions(questionnaire))

    def test_country_knows_its_data_submitter(self):
        questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013)
        section_1 = Section.objects.create(title="Cover PAge", order=1,
                                           questionnaire=questionnaire, name="Cover Pages")
        sub_section = SubSection.objects.create(title="Details", order=1, section=section_1)
        question = Question.objects.create(text='Name of person in Ministry of Health', UID='C00054', answer_type='Number')
        parent = QuestionGroup.objects.create(subsection=sub_section, order=1)
        parent.question.add(question)

        organisation = Organization.objects.create(name="WHO")
        afro = Region.objects.create(name="Afro", organization=organisation)
        uganda = Country.objects.create(name="Uganda", code="UGX")
        afro.countries.add(uganda)
        TextAnswer.objects.create(question=question, response="jacinta",status=Answer.DRAFT_STATUS,country=uganda)

        self.assertEqual('jacinta', uganda.data_submitter())

    def test_gets_versions_for_a__list_of_questionnaires(self):
        answer = NumericalAnswer.objects.create(question=self.question2, country=self.uganda, status=Answer.DRAFT_STATUS,
                                       response=22)
        questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013)
        section_1 = Section.objects.create(title="Cover PAge", order=1,
                                           questionnaire=questionnaire, name="Cover Pages")
        self.assertEqual({self.questionnaire: [answer.version], questionnaire: []}, self.uganda.get_versions_for([self.questionnaire, questionnaire]))


class OrgTest(BaseTest):

    def test_org_fields(self):
        org = Organization()
        fields = [str(item.attname) for item in org._meta.fields]
        self.assertEqual(4, len(fields))
        for field in ['id', 'created', 'modified', 'name']:
            self.assertIn(field, fields)

    def test_store(self):
        org = Organization.objects.create(name="WHO")
        self.failUnless(org.id)
        self.assertEqual("WHO", org.name)
