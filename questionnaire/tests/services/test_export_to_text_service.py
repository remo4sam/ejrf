from questionnaire.models import Question, QuestionGroup, Questionnaire, SubSection, Section, Answer, Country, \
    Organization, Region, NumericalAnswer, QuestionOption, MultiChoiceAnswer, AnswerGroup, TextAnswer, QuestionGroupOrder, Theme
from questionnaire.services.export_data_service import ExportToTextService
from questionnaire.tests.base_test import BaseTest


class ExportToTextServiceTest(BaseTest):
    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English",
                                                          description="From dropbox as given by Rouslan", year=2013)
        self.section_1 = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)",
                                                order=1,
                                                questionnaire=self.questionnaire, name="Reported Cases")

        self.sub_section = SubSection.objects.create(title="Reported cases for the year 2013", order=1,
                                                     section=self.section_1)
        self.primary_question = Question.objects.create(text='Disease', UID='C00003', answer_type='MultiChoice',
                                                        is_primary=True)
        self.option = QuestionOption.objects.create(text="Measles", question=self.primary_question, UID="QO1")
        self.option2 = QuestionOption.objects.create(text="TB", question=self.primary_question, UID="QO2")

        self.question1 = Question.objects.create(text='B. Number of cases tested', UID='C00004', answer_type='Number')

        self.question2 = Question.objects.create(text='C. Number of cases positive',
                                                 instructions="Include only those cases found positive for the infectious agent.",
                                                 UID='C00005', answer_type='Number')

        self.parent = QuestionGroup.objects.create(subsection=self.sub_section, order=1)
        self.parent.question.add(self.question1, self.question2, self.primary_question)
        self.organisation = Organization.objects.create(name="WHO")
        self.regions = Region.objects.create(name="The Afro", organization=self.organisation)
        self.country = Country.objects.create(name="Uganda", code="UGX")
        self.regions.countries.add(self.country)
        self.headings = "ISO\tCountry\tYear\tField code\tQuestion text\tValue"

        self.primary_question_answer = MultiChoiceAnswer.objects.create(question=self.primary_question,
                                                                        country=self.country,
                                                                        status=Answer.SUBMITTED_STATUS,
                                                                        response=self.option)
        self.question1_answer = NumericalAnswer.objects.create(question=self.question1, country=self.country,
                                                               status=Answer.SUBMITTED_STATUS, response=23)
        self.question2_answer = NumericalAnswer.objects.create(question=self.question2, country=self.country,
                                                               status=Answer.SUBMITTED_STATUS, response=1)
        self.answer_group1 = self.primary_question_answer.answergroup.create(grouped_question=self.parent, row=1)
        self.answer_group_1 = self.question1_answer.answergroup.create(grouped_question=self.parent, row=1)
        self.answer_group_2 = self.question2_answer.answergroup.create(grouped_question=self.parent, row=1)

        QuestionGroupOrder.objects.create(question=self.primary_question, question_group=self.parent, order=1)
        QuestionGroupOrder.objects.create(question=self.question1, question_group=self.parent, order=2)
        QuestionGroupOrder.objects.create(question=self.question2, question_group=self.parent, order=3)

    def test_exports_questions_with_numeric_answers(self):
        question_text = "%s | %s | %s" % (self.section_1.title, self.sub_section.title, self.primary_question.text)
        question_text1 = "%s | %s | %s" % (self.section_1.title, self.sub_section.title, self.question1.text)
        question_text_2 = "%s | %s | %s" % (self.section_1.title, self.sub_section.title, self.question2.text)
        answer_id = "C_%s_%s_%s" % (self.primary_question.UID, self.primary_question.UID, self.option.UID)
        answer_id_1 = "C_%s_%s_1" % (self.primary_question.UID, self.question1.UID)
        answer_id_2 = "C_%s_%s_%d_1" % (self.primary_question.UID, self.question1.UID, 1)
        expected_data = [self.headings,
                         "UGX\t%s\t2013\t%s\t%s\t%s" % (
                         self.country.name, answer_id.encode('base64').strip(), question_text, self.option.text),
                         "UGX\t%s\t2013\t%s\t%s\t%s" % (
                         self.country.name, answer_id_1.encode('base64').strip(), question_text1, '23.00'),
                         "UGX\t%s\t2013\t%s\t%s\t%s" % (
                         self.country.name, answer_id_2.encode('base64').strip(), question_text_2, '1.00')]

        export_to_text_service = ExportToTextService(self.questionnaire)
        actual_data = export_to_text_service.get_formatted_responses()
        self.assertEqual(len(expected_data), len(actual_data))
        self.assertIn(expected_data[0], actual_data)
        self.assertIn(expected_data[1], actual_data)

    def test_exports_questions_with_two_versions(self):
        primary_question_answer2 = MultiChoiceAnswer.objects.create(question=self.primary_question,
                                                                    country=self.country,
                                                                    status=Answer.SUBMITTED_STATUS,
                                                                    response=self.option2)
        question1_answer2 = NumericalAnswer.objects.create(question=self.question1, country=self.country,
                                                           status=Answer.SUBMITTED_STATUS, response=4)
        question2_answer2 = NumericalAnswer.objects.create(question=self.question2, country=self.country,
                                                           status=Answer.SUBMITTED_STATUS, response=55)
        answer_group2 = primary_question_answer2.answergroup.create(grouped_question=self.parent, row=2)
        answer_group2_1 = question1_answer2.answergroup.create(grouped_question=self.parent, row=2)
        answer_group2_2 = question2_answer2.answergroup.create(grouped_question=self.parent, row=2)

        question_text = "%s | %s | %s" % (self.section_1.title, self.sub_section.title, self.primary_question.text)
        question_text1 = "%s | %s | %s" % (self.section_1.title, self.sub_section.title, self.question1.text)
        question_text_2 = "%s | %s | %s" % (self.section_1.title, self.sub_section.title, self.question2.text)
        answer_id = "C_%s_%s_%s" % (self.primary_question.UID, self.primary_question.UID, self.option.UID)
        answer_id_1 = "C_%s_%s_1" % (self.primary_question.UID, self.question1.UID)
        answer_id_2 = "C_%s_%s_1" % (self.primary_question.UID, self.question2.UID)
        answer_id_10 = "C_%s_%s_%s" % (self.primary_question.UID, self.primary_question.UID, self.option2.UID)
        answer_id_11 = "C_%s_%s_2" % (self.primary_question.UID, self.question1.UID)
        answer_id_21 = "C_%s_%s_2" % (self.primary_question.UID, self.question2.UID)
        expected_data = [self.headings,
                         "UGX\t%s\t2013\t%s\t%s\t%s" % (
                         self.country.name, answer_id.encode('base64').strip(), question_text, self.option.text),
                         "UGX\t%s\t2013\t%s\t%s\t%s" % (
                         self.country.name, answer_id_1.encode('base64').strip(), question_text1, '23.00'),
                         "UGX\t%s\t2013\t%s\t%s\t%s" % (
                         self.country.name, answer_id_2.encode('base64').strip(), question_text_2, '1.00'),
                         "UGX\t%s\t2013\t%s\t%s\t%s" % (
                         self.country.name, answer_id_10.encode('base64').strip(), question_text, self.option2.text),
                         "UGX\t%s\t2013\t%s\t%s\t%s" % (
                         self.country.name, answer_id_11.encode('base64').strip(), question_text1, '4.00'),
                         "UGX\t%s\t2013\t%s\t%s\t%s" % (
                         self.country.name, answer_id_21.encode('base64').strip(), question_text_2, '55.00')]

        export_to_text_service = ExportToTextService(self.questionnaire)
        actual_data = export_to_text_service.get_formatted_responses()

        self.assertEqual(len(expected_data), len(actual_data))
        self.assertIn(expected_data[0], actual_data)
        self.assertIn(expected_data[1], actual_data)
        self.assertIn(expected_data[2], actual_data)
        self.assertIn(expected_data[3], actual_data)
        self.assertIn(expected_data[4], actual_data)
        self.assertIn(expected_data[5], actual_data)

    def test_exports_specific_version(self):
        primary_question_answer2 = MultiChoiceAnswer.objects.create(question=self.primary_question,
                                                                    country=self.country,
                                                                    status=Answer.SUBMITTED_STATUS,
                                                                    response=self.option2, version=2)
        question1_answer2 = NumericalAnswer.objects.create(question=self.question1, country=self.country,
                                                           status=Answer.SUBMITTED_STATUS, response=4, version=2)
        question2_answer2 = NumericalAnswer.objects.create(question=self.question2, country=self.country,
                                                           status=Answer.SUBMITTED_STATUS, response=55, version=2)
        answer_group2 = primary_question_answer2.answergroup.create(grouped_question=self.parent, row=2)
        answer_group2_1 = question1_answer2.answergroup.create(grouped_question=self.parent, row=2)
        answer_group2_2 = question2_answer2.answergroup.create(grouped_question=self.parent, row=2)

        question_text = "%s | %s | %s" % (self.section_1.title, self.sub_section.title, self.primary_question.text)
        question_text1 = "%s | %s | %s" % (self.section_1.title, self.sub_section.title, self.question1.text)
        question_text_2 = "%s | %s | %s" % (self.section_1.title, self.sub_section.title, self.question2.text)
        answer_id = "C_%s_%s_%s" % (self.primary_question.UID, self.primary_question.UID, self.option2.UID)
        answer_id_1 = "C_%s_%s_2" % (self.primary_question.UID, self.question1.UID)
        answer_id_2 = "C_%s_%s_2" % (self.primary_question.UID, self.question2.UID)

        expected_data = [self.headings,
                         "UGX\t%s\t2013\t%s\t%s\t%s" % (
                         self.country.name, answer_id.encode('base64').strip(), question_text, self.option2.text),
                         "UGX\t%s\t2013\t%s\t%s\t%s" % (
                         self.country.name, answer_id_1.encode('base64').strip(), question_text1, '4.00'),
                         "UGX\t%s\t2013\t%s\t%s\t%s" % (
                         self.country.name, answer_id_2.encode('base64').strip(), question_text_2, '55.00')]

        export_to_text_service = ExportToTextService(self.questionnaire, version=2)
        actual_data = export_to_text_service.get_formatted_responses()
        self.assertEqual(len(expected_data), len(actual_data))
        self.assertIn(expected_data[0], actual_data)
        self.assertIn(expected_data[1], actual_data)

    def test_exports_specific_country(self):
        ghana = Country.objects.create(name="Ghana", code="GH")
        primary_question_answer2 = MultiChoiceAnswer.objects.create(question=self.primary_question, country=ghana,
                                                                    status=Answer.SUBMITTED_STATUS,
                                                                    response=self.option2, version=2)
        question1_answer2 = NumericalAnswer.objects.create(question=self.question1, country=ghana,
                                                           status=Answer.SUBMITTED_STATUS, response=4, version=2)
        question2_answer2 = NumericalAnswer.objects.create(question=self.question2, country=ghana,
                                                           status=Answer.SUBMITTED_STATUS, response=55, version=2)
        answer_group2 = primary_question_answer2.answergroup.create(grouped_question=self.parent, row=2)
        answer_group2_1 = question1_answer2.answergroup.create(grouped_question=self.parent, row=2)
        answer_group2_2 = question2_answer2.answergroup.create(grouped_question=self.parent, row=2)

        question_text = "%s | %s | %s" % (self.section_1.title, self.sub_section.title, self.primary_question.text)
        question_text1 = "%s | %s | %s" % (self.section_1.title, self.sub_section.title, self.question1.text)
        question_text_2 = "%s | %s | %s" % (self.section_1.title, self.sub_section.title, self.question2.text)
        answer_id = "C_%s_%s_%s" % (self.primary_question.UID, self.primary_question.UID, self.option2.UID)
        answer_id_1 = "C_%s_%s_2" % (self.primary_question.UID, self.question1.UID)
        answer_id_2 = "C_%s_%s_2" % (self.primary_question.UID, self.question2.UID)

        expected_data = [self.headings,
                         "%s\t%s\t2013\t%s\t%s\t%s" % (
                         ghana.code, ghana.name, answer_id.encode('base64').strip(), question_text, self.option2.text),
                         "%s\t%s\t2013\t%s\t%s\t%s" % (
                         ghana.code, ghana.name, answer_id_1.encode('base64').strip(), question_text1, '4.00'),
                         "%s\t%s\t2013\t%s\t%s\t%s" % (
                         ghana.code, ghana.name, answer_id_2.encode('base64').strip(), question_text_2, '55.00')]

        export_to_text_service = ExportToTextService(self.questionnaire, countries=ghana)
        actual_data = export_to_text_service.get_formatted_responses()
        self.assertEqual(len(expected_data), len(actual_data))
        self.assertIn(expected_data[0], actual_data)
        self.assertIn(expected_data[1], actual_data)

    def test_exports_single_question_in_a_group_questionnaire(self):
        Question.objects.all().delete()
        question = Question.objects.create(text='what do you drink?', UID='abc123', answer_type='Text')
        parent = QuestionGroup.objects.create(subsection=self.sub_section, order=2)
        parent.question.add(question)

        QuestionGroupOrder.objects.create(question=question, question_group=parent, order=1)

        country = Country.objects.create(name="Uganda", code="UGX")
        answer1 = TextAnswer.objects.create(question=question, country=country, response="tusker lager",
                                            status=Answer.SUBMITTED_STATUS)

        answer_group1 = AnswerGroup.objects.create(grouped_question=parent, row=1)
        answer_group1.answer.add(answer1)

        question_text = "%s | %s | %s" % (self.section_1.title, self.sub_section.title, question.text)
        answer_id = "C_%s_%s_1" % (question.UID, question.UID)

        expected_data = [self.headings,
                         "UGX\t%s\t2013\t%s\t%s\t%s" % (
                         self.country.name, answer_id.encode('base64').strip(), question_text, 'tusker lager')]

        export_to_text_service = ExportToTextService(self.questionnaire)
        actual_data = export_to_text_service.get_formatted_responses()
        self.assertEqual(len(expected_data), len(actual_data))
        self.assertIn(expected_data[0], actual_data)

    def test_draft_answers_does_not_show_on_extract_questionnaire_answers(self):
        Question.objects.all().delete()
        question = Question.objects.create(text='what do you drink?', UID='abc123', answer_type='Text')
        parent = QuestionGroup.objects.create(subsection=self.sub_section, order=2)
        parent.question.add(question)

        QuestionGroupOrder.objects.create(question=question, question_group=parent, order=1)

        country = Country.objects.create(name="Uganda", code="UGX")
        answer1 = TextAnswer.objects.create(question=question, country=country, response="tusker lager",
                                            status=Answer.DRAFT_STATUS)

        answer_group1 = AnswerGroup.objects.create(grouped_question=parent, row=1)
        answer_group1.answer.add(answer1)

        expected_data = [self.headings, ]

        export_to_text_service = ExportToTextService(self.questionnaire)
        actual_data = export_to_text_service.get_formatted_responses()
        self.assertEqual(len(expected_data), len(actual_data))
        self.assertIn(expected_data[0], actual_data)


class GRIDQuestionsExportTest(BaseTest):
    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English",
                                                          description="From dropbox as given by Rouslan", year=2013)
        self.section_1 = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)",
                                                order=1,
                                                questionnaire=self.questionnaire, name="Reported Cases")

        self.sub_section = SubSection.objects.create(title="Reported cases for the year 2013", order=1,
                                                     section=self.section_1)
        self.primary_question = Question.objects.create(text='Disease', UID='C00003', answer_type='MultiChoice',
                                                        is_primary=True)
        self.option = QuestionOption.objects.create(text="Measles", question=self.primary_question, UID="QO1")
        self.option2 = QuestionOption.objects.create(text="TB", question=self.primary_question, UID="QO2")

        self.question1 = Question.objects.create(text='B. Number of cases tested', UID='C00004', answer_type='Number')

        self.question2 = Question.objects.create(text='C. Number of cases positive',
                                                 instructions="Include only those cases found positive for the infectious agent.",
                                                 UID='C00005', answer_type='Number')

        self.parent = QuestionGroup.objects.create(subsection=self.sub_section, order=1, grid=True, display_all=True)
        self.parent.question.add(self.question1, self.question2, self.primary_question)
        QuestionGroupOrder.objects.create(question=self.primary_question, question_group=self.parent, order=1)
        QuestionGroupOrder.objects.create(question=self.question1, question_group=self.parent, order=2)
        QuestionGroupOrder.objects.create(question=self.question2, question_group=self.parent, order=3)

        self.organisation = Organization.objects.create(name="WHO")
        self.regions = Region.objects.create(name="The Afro", organization=self.organisation)
        self.country = Country.objects.create(name="Uganda", code="UGX")
        self.regions.countries.add(self.country)
        self.headings = "ISO\tCountry\tYear\tField code\tQuestion text\tValue"

        self.primary_question_answer = MultiChoiceAnswer.objects.create(question=self.primary_question,
                                                                        country=self.country,
                                                                        status=Answer.SUBMITTED_STATUS,
                                                                        response=self.option)
        self.question1_answer = NumericalAnswer.objects.create(question=self.question1, country=self.country,
                                                               status=Answer.SUBMITTED_STATUS, response=23)
        self.question2_answer = NumericalAnswer.objects.create(question=self.question2, country=self.country,
                                                               status=Answer.SUBMITTED_STATUS, response=1)
        self.answer_group1 = self.primary_question_answer.answergroup.create(grouped_question=self.parent, row=1)
        self.answer_group1.answer.add(self.question1_answer, self.question2_answer)

        self.primary_question_answer2 = MultiChoiceAnswer.objects.create(question=self.primary_question,
                                                                         country=self.country,
                                                                         status=Answer.SUBMITTED_STATUS,
                                                                         response=self.option2)
        self.question1_answer2 = NumericalAnswer.objects.create(question=self.question1, country=self.country,
                                                                status=Answer.SUBMITTED_STATUS, response=3)
        self.question2_answer2 = NumericalAnswer.objects.create(question=self.question2, country=self.country,
                                                                status=Answer.SUBMITTED_STATUS, response=12)
        self.answer_group2 = self.primary_question_answer2.answergroup.create(grouped_question=self.parent, row=2)
        self.answer_group2.answer.add(self.question1_answer2, self.question2_answer2)

    def test_grid_display_all_answers(self):
        question_text = "%s | %s | %s" % (self.section_1.title, self.sub_section.title, self.primary_question.text)
        question_text1 = "%s | %s | %s" % (self.section_1.title, self.sub_section.title, self.question1.text)
        question_text_2 = "%s | %s | %s" % (self.section_1.title, self.sub_section.title, self.question2.text)
        answer_id = "C_%s_%s_%s" % (self.primary_question.UID, self.primary_question.UID, self.option.UID)
        answer_id_1 = "C_%s_%s_1" % (self.primary_question.UID, self.question1.UID)
        answer_id_2 = "C_%s_%s_1" % (self.primary_question.UID, self.question2.UID)
        answer_id_10 = "C_%s_%s_%s" % (self.primary_question.UID, self.primary_question.UID, self.option2.UID)
        answer_id_11 = "C_%s_%s_2" % (self.primary_question.UID, self.question1.UID)
        answer_id_21 = "C_%s_%s_2" % (self.primary_question.UID, self.question2.UID)
        expected_data = [self.headings,
                         "UGX\t%s\t2013\t%s\t%s\t%s" % (
                         self.country.name, answer_id.encode('base64').strip(), question_text, self.option.text),
                         "UGX\t%s\t2013\t%s\t%s\t%s" % (
                         self.country.name, answer_id_1.encode('base64').strip(), question_text1, '23.00'),
                         "UGX\t%s\t2013\t%s\t%s\t%s" % (
                         self.country.name, answer_id_2.encode('base64').strip(), question_text_2, '1.00'),
                         "UGX\t%s\t2013\t%s\t%s\t%s" % (
                         self.country.name, answer_id_10.encode('base64').strip(), question_text, self.option2.text),
                         "UGX\t%s\t2013\t%s\t%s\t%s" % (
                         self.country.name, answer_id_11.encode('base64').strip(), question_text1, '3.00'),
                         "UGX\t%s\t2013\t%s\t%s\t%s" % (
                         self.country.name, answer_id_21.encode('base64').strip(), question_text_2, '12.00')]

        export_to_text_service = ExportToTextService(self.questionnaire)
        actual_data = export_to_text_service.get_formatted_responses()

        self.assertEqual(len(expected_data), len(actual_data))
        self.assertIn(expected_data[0], actual_data)
        self.assertIn(expected_data[1], actual_data)
        self.assertIn(expected_data[2], actual_data)
        self.assertIn(expected_data[3], actual_data)
        self.assertIn(expected_data[4], actual_data)
        self.assertIn(expected_data[5], actual_data)


class ExportCustomFieldsToTextServiceTest(BaseTest):
    def setUp(self):
        self.organisation = Organization.objects.create(name="WHO")
        self.regions = Region.objects.create(name="The Afro", organization=self.organisation)
        self.regions_2 = Region.objects.create(name="The Amr", organization=self.organisation)
        self.country = Country.objects.create(name="Uganda", code="UGX")
        self.country_2 = Country.objects.create(name="Brazil", code="RAEL")
        self.regions.countries.add(self.country)
        self.regions_2.countries.add(self.country_2)
        self.headings = "ISO\tCountry\tYear\tField code\tQuestion text\tValue"

        self.theme = Theme.objects.create(name="First theme", description="This is a wonderful decription")
        self.theme1 = Theme.objects.create(name="Second theme", description="This is a second wonderful decription")
        self.questionnaire, self.section, self.subsection = self.setup_create_questionnaire_and_answers(name="JRF 2013 Core English",
                                                             year=2013, theme=self.theme)

        self.questionnaire2, self.section_2, self.subsection_2 = self.setup_create_questionnaire_and_answers(name="JRF 2014 Core English",
                                                              year=2014, theme=self.theme1)

    def setup_create_questionnaire_and_answers(self, name, year, theme=None):
        questionnaire = Questionnaire.objects.create(name=name,
                                                    description="Description",
                                                    year=year)
        section_1 = Section.objects.create(title="section_1",
                                                order=1,
                                                questionnaire=questionnaire, name="Reported Cases")
        sub_section = SubSection.objects.create(title="sun section one", order=1,
                                                     section=section_1)

        question1 = Question.objects.create(text='B. Number of cases tested', UID='C5' + str(year),
                                                 answer_type='Number',
                                                 theme=theme)
        question2 = Question.objects.create(text='C. Number of cases positive',
                                                 instructions="Include only those cases found positive for the infectious agent.",
                                                 UID='C6' + str(year), answer_type='Number', theme=theme)

        question3 = Question.objects.create(text='primary_question', UID='C4' + str(year), answer_type='MultiChoice',
                                                        is_primary=True, theme=theme)
        option = QuestionOption.objects.create(text="Measles", question=question3, UID="Q3" + str(year))
        option2 = QuestionOption.objects.create(text="TB", question=question3, UID="Q4" + str(year))

        question_group = QuestionGroup.objects.create(subsection=sub_section, order=1)
        question_group.question.add(question1, question2, question3)


        def setup_create_answers():
            question1_answer = NumericalAnswer.objects.create(question=question1, country=self.country,
                                                              status=Answer.SUBMITTED_STATUS, response=23)

            question2_answer = NumericalAnswer.objects.create(question=question2, country=self.country,
                                                              status=Answer.SUBMITTED_STATUS, response=1)

            question3_answer = MultiChoiceAnswer.objects.create(question=question3,
                                                                       country=self.country,
                                                                       status=Answer.SUBMITTED_STATUS,
                                                                       response=option)
            answer_group_1 = question1_answer.answergroup.create(grouped_question=question_group, row=1)
            answer_group_2 = question2_answer.answergroup.create(grouped_question=question_group, row=1)
            answer_group1 = question3_answer.answergroup.create(grouped_question=question_group, row=1)

            QuestionGroupOrder.objects.create(question=question3, question_group=question_group, order=1)
            QuestionGroupOrder.objects.create(question=question1, question_group=question_group, order=2)
            QuestionGroupOrder.objects.create(question=question2, question_group=question_group, order=3)

        setup_create_answers()
        return questionnaire, section_1, sub_section

    def test_export_questions_and_answers_for_two_questionnaires(self):
        expected_data = [self.headings]
        line_format = "UGX\t%s\t2013\t%s\t%s\t%s"

        #questionnaire 1
        for number in range(0, 3, 1):
            question = self.subsection.all_questions()[number]
            question_text = "%s | %s | %s" % (self.section.title, self.subsection.title, question.text)
            answer_id = "C_%s_%s_1" % (question.UID, question.UID)
            expected_data.append(line_format % (self.country.name, answer_id.encode('base64').strip(), question_text, '23'))

        # questionnaire 2
        for number in range(0, 3, 1):
            question = self.subsection_2.all_questions()[number]
            question_text = "%s | %s | %s" % (self.section_2.title, self.subsection_2.title, question.text)
            answer_id = "C_%s_%s_1" % (question.UID, question.UID)
            expected_data.append(line_format % (self.country.name, answer_id.encode('base64').strip(), question_text, '23'))

        export_to_text_service = ExportToTextService(questionnaire=[self.questionnaire,self.questionnaire2])
        actual_data = export_to_text_service.get_formatted_responses()
        self.assertEqual(len(expected_data), len(actual_data))
        self.assertIn(expected_data[0], actual_data)

