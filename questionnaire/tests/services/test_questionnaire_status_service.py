from questionnaire.models import Question, QuestionGroup, Questionnaire, SubSection, Section, Country, \
    Organization, Region, QuestionOption, MultiChoiceAnswer, NumericalAnswer, AnswerGroup, Answer
from questionnaire.services.questionnaire_status import QuestionnaireStatusService, Status
from questionnaire.tests.base_test import BaseTest


class QuestionnaireStatusServiceTest(BaseTest):

    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013)
        self.section_1 = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)", order=1,
                                                      questionnaire=self.questionnaire, name="Reported Cases")

        self.sub_section = SubSection.objects.create(title="Reported cases for the year 2013", order=1, section=self.section_1)
        self.primary_question = Question.objects.create(text='Disease', UID='C00003', answer_type='MultiChoice',
                                                        is_primary=True)
        self.option = QuestionOption.objects.create(text="Measles", question=self.primary_question, UID="QO1")
        self.option2 = QuestionOption.objects.create(text="TB", question=self.primary_question, UID="QO2")
        self.question1 = Question.objects.create(text='B. Number of cases tested', UID='C00004', answer_type='Number')
        self.question2 = Question.objects.create(text='C. Number of cases positive', UID='C00005', answer_type='Number')

        self.parent = QuestionGroup.objects.create(subsection=self.sub_section, order=1)
        self.parent.question.add(self.question1, self.question2, self.primary_question)
        self.organisation = Organization.objects.create(name="WHO")

        self.afro = Region.objects.create(name="Afro", organization=self.organisation)
        self.uganda = Country.objects.create(name="Uganda", code="UGX")
        self.rwanda = Country.objects.create(name="Rwanda", code="RWA")
        self.afro.countries.add(self.uganda, self.rwanda)

        self.asean = Region.objects.create(name="Asean", organization=self.organisation)
        self.singapore = Country.objects.create(name="Singapore", code="SNP")
        self.malyasia = Country.objects.create(name="Malyasia", code="MLS")
        self.asean.countries.add(self.malyasia, self.singapore)

        self.paho = Region.objects.create(name="PAHO", organization=self.organisation)
        self.peru = Country.objects.create(name="Peru", code="PRU")
        self.argentina = Country.objects.create(name="Argentina", code="ARG")
        self.paho.countries.add(self.peru, self.argentina)

    def test_returns_not_started_for_all_regions_if_none_has_answered(self):
        paho_status = {self.argentina: Status.options[None], self.peru: Status.options[None]}
        afro_status = {self.rwanda: Status.options[None], self.uganda: Status.options[None]}
        asean_status = {self.malyasia: Status.options[None], self.singapore: Status.options[None]}
        questionnaire_statuses = QuestionnaireStatusService(self.questionnaire).region_country_status_map()

        self.assertEqual(afro_status, questionnaire_statuses[self.afro])
        self.assertEqual(asean_status, questionnaire_statuses[self.asean])
        self.assertEqual(paho_status, questionnaire_statuses[self.paho])

    def test_returns_not_started_for_all_regions_if_started_if_country_in_region_has_drafts(self):
        MultiChoiceAnswer.objects.create(question=self.primary_question, country=self.peru,
                                         status=Answer.DRAFT_STATUS,  response=self.option)
        MultiChoiceAnswer.objects.create(question=self.primary_question, country=self.argentina,
                                         status=Answer.SUBMITTED_STATUS,  response=self.option)
        NumericalAnswer.objects.create(question=self.question1, country=self.uganda,
                                       status=Answer.SUBMITTED_STATUS,  response=23)
        NumericalAnswer.objects.create(question=self.question2, country=self.singapore,
                                       status=Answer.DRAFT_STATUS, response=1)

        paho_status = {self.argentina: Status.options['Submitted'], self.peru: Status.options['Draft']}
        afro_status = {self.rwanda: Status.options[None], self.uganda: Status.options['Submitted']}
        asean_status = {self.malyasia: Status.options[None], self.singapore: Status.options['Draft']}
        questionnaire_statuses = QuestionnaireStatusService(self.questionnaire).region_country_status_map()

        self.assertEqual(afro_status, questionnaire_statuses[self.afro])
        self.assertEqual(asean_status, questionnaire_statuses[self.asean])
        self.assertEqual(paho_status, questionnaire_statuses[self.paho])