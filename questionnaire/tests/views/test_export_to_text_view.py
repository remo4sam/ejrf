from urllib import quote
from django.test import Client
from questionnaire.models import Questionnaire, Section, SubSection, Question, QuestionGroup, Organization, Region, Country, NumericalAnswer, Answer, QuestionGroupOrder, AnswerGroup, \
    MultiChoiceAnswer, QuestionOption, Theme
from questionnaire.tests.base_test import BaseTest


class ExportToTextViewTest(BaseTest):
    def setUp(self):
        self.client = Client()
        self.user, self.country, self.region = self.create_user_with_no_permissions()
        self.login_user()

        self.organisation = Organization.objects.create(name="WHO")
        self.regions = Region.objects.create(name="The Afro", organization=self.organisation)
        self.country = Country.objects.create(name="Uganda", code="UGX")
        self.regions.countries.add(self.country)

        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English",
                                                          description="From dropbox as given by Rouslan",
                                                          year=2013, region = self.regions)
        self.section_1 = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)",
                                                order=1,
                                                questionnaire=self.questionnaire, name="Reported Cases")

        self.sub_section = SubSection.objects.create(title="Reported cases for the year 2013", order=1,
                                                     section=self.section_1)

        self.theme = Theme.objects.create(name = "Theme1", description="Some Theme")

        self.question1 = Question.objects.create(text='B. Number of cases tested',
                                                 instructions="Enter the total number of cases for which specimens were collected, and tested in laboratory",
                                                 UID='C00003', answer_type='Number', theme=self.theme)

        self.question2 = Question.objects.create(text='C. Number of cases positive',
                                                 instructions="Include only those cases found positive for the infectious agent.",
                                                 UID='C00004', answer_type='Number', theme=self.theme)

        self.parent = QuestionGroup.objects.create(subsection=self.sub_section, order=1)
        self.parent.question.add(self.question1, self.question2)


        self.question1_answer = NumericalAnswer.objects.create(question=self.question1, country=self.country,
                                                               status=Answer.SUBMITTED_STATUS, response=23)
        self.question2_answer = NumericalAnswer.objects.create(question=self.question2, country=self.country,
                                                               status=Answer.SUBMITTED_STATUS, response=1)

        self.answer_group1 = AnswerGroup.objects.create(grouped_question=self.parent, row=1)
        self.answer_group1.answer.add(self.question1_answer, self.question2_answer)

        QuestionGroupOrder.objects.create(question=self.question1, question_group=self.parent, order=2)
        QuestionGroupOrder.objects.create(question=self.question2, question_group=self.parent, order=3)

    def test_get(self):
        response = self.client.get("/extract/")
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('home/extract.html', templates)
        self.assertIn(self.questionnaire, response.context['questionnaires'])

    def test_login_required_for_home_get(self):
        self.client.logout()
        response = self.client.get("/extract/")
        self.assertRedirects(response, expected_url='accounts/login/?next=%s' % quote('/extract/'), status_code=302)

    def test_post_export(self):
        form_data = {'questionnaire': self.questionnaire.id, 'years': {'2013', '2014'}, 'regions': self.regions.id,
                     'countries': self.country.id, 'themes': self.theme.id}

        file_name = "%s-%s.txt" % ('data', '2014_2013')
        response = self.client.post('/extract/', data=form_data)
        self.assertEquals(200, response.status_code)
        self.assertEquals(response.get('Content-Type'), 'text/csv')
        self.assertEquals(response.get('Content-Disposition'), 'attachment; filename="%s"' % file_name)

        question_text1 = "%s | %s | %s" % (self.section_1.title, self.sub_section.title, self.question1.text)
        question_text_2 = "%s | %s | %s" % (self.section_1.title, self.sub_section.title, self.question2.text)
        answer_id_1 = "C_%s_%s_1" % (self.question1.UID, self.question1.UID)
        answer_id_2 = "C_%s_%s_%d" % (self.question1.UID, self.question2.UID, 1)
        headings = "ISO\tCountry\tYear\tField code\tQuestion text\tValue"
        row1 = "UGX\t%s\t2013\t%s\t%s\t%s" % (self.country.name, answer_id_1.encode('base64').strip(), question_text1, '23.00')
        row2 = "UGX\t%s\t2013\t%s\t%s\t%s" % (self.country.name, answer_id_2.encode('base64').strip(), question_text_2, '1.00')
        contents = "%s\r\n%s\r\n%s" % ("".join(headings), "".join(row1), "".join(row2))

        self.assertEqual(contents, response.content)


class SpecificExportViewTest(BaseTest):
    def setUp(self):
        self.client = Client()
        self.user, self.country, self.region = self.create_user_with_no_permissions()
        self.login_user()

        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", description="From dropbox as given by Rouslan",
                                                          year=2013, status=Questionnaire.PUBLISHED, region=self.region)
        self.section_1 = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)", order=1,
                                                      questionnaire=self.questionnaire, name="Reported Cases")

        self.sub_section = SubSection.objects.create(title="Reported cases for the year 2013", order=1, section=self.section_1)
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

        self.primary_question_answer = MultiChoiceAnswer.objects.create(question=self.primary_question, country=self.country,
                                                               status=Answer.SUBMITTED_STATUS,  response=self.option)
        self.question1_answer = NumericalAnswer.objects.create(question=self.question1, country=self.country,
                                                               status=Answer.SUBMITTED_STATUS,  response=23)
        self.question2_answer = NumericalAnswer.objects.create(question=self.question2, country=self.country,
                                                               status=Answer.SUBMITTED_STATUS, response=1)
        self.answer_group1 = self.primary_question_answer.answergroup.create(grouped_question=self.parent, row=1)
        self.answer_group_1 = self.question1_answer.answergroup.create(grouped_question=self.parent, row=1)
        self.answer_group_2 = self.question2_answer.answergroup.create(grouped_question=self.parent, row=1)

        QuestionGroupOrder.objects.create(question=self.primary_question, question_group=self.parent, order=1)
        QuestionGroupOrder.objects.create(question=self.question1, question_group=self.parent, order=2)
        QuestionGroupOrder.objects.create(question=self.question2, question_group=self.parent, order=3)

    def test_post_specific_export(self):
        ghana = Country.objects.create(name="Ghana", code="GH")
        self.region.countries.add(ghana)
        primary_question_answer2 = MultiChoiceAnswer.objects.create(question=self.primary_question, country=ghana,
                                                                    status=Answer.SUBMITTED_STATUS,  response=self.option2, version=2)
        question1_answer2 = NumericalAnswer.objects.create(question=self.question1, country=ghana,
                                                           status=Answer.SUBMITTED_STATUS,  response=4, version=2)
        question2_answer2 = NumericalAnswer.objects.create(question=self.question2, country=ghana,
                                                           status=Answer.SUBMITTED_STATUS, response=55, version=2)
        answer_group2 = primary_question_answer2.answergroup.create(grouped_question=self.parent, row=2)
        answer_group2_1 = question1_answer2.answergroup.create(grouped_question=self.parent, row=2)
        answer_group2_2 = question2_answer2.answergroup.create(grouped_question=self.parent, row=2)

        file_name = "%s-%s-%s-%s.txt" % (self.questionnaire.name, self.questionnaire.year, ghana.name, 2)
        response = self.client.post('/extract/country/%d/version/%d/'%(ghana.id, 2))
        self.assertEquals(200, response.status_code)
        self.assertEquals(response.get('Content-Type'), 'text/csv')
        self.assertEquals(response.get('Content-Disposition'), 'attachment; filename="%s"' % file_name)

        question_text = "%s | %s | %s" % (self.section_1.title, self.sub_section.title, self.primary_question.text)
        question_text1 = "%s | %s | %s" % (self.section_1.title, self.sub_section.title, self.question1.text)
        question_text_2 = "%s | %s | %s" % (self.section_1.title, self.sub_section.title, self.question2.text)
        answer_id = "C_%s_%s_%s" % (self.primary_question.UID, self.primary_question.UID, self.option2.UID)
        answer_id_1 = "C_%s_%s_2" % (self.primary_question.UID, self.question1.UID)
        answer_id_2 = "C_%s_%s_2" % (self.primary_question.UID, self.question2.UID)

        expected_data = [self.headings,
                         "%s\t%s\t2013\t%s\t%s\t%s" % (ghana.code, ghana.name, answer_id.encode('base64').strip(), question_text, self.option2.text),
                         "%s\t%s\t2013\t%s\t%s\t%s" % (ghana.code, ghana.name, answer_id_1.encode('base64').strip(), question_text1, '4.00'),
                         "%s\t%s\t2013\t%s\t%s\t%s" % (ghana.code, ghana.name, answer_id_2.encode('base64').strip(), question_text_2, '55.00')]

        contents = "%s\r\n%s\r\n%s\r\n%s" % ("".join(expected_data[0]), "".join(expected_data[1]),
                                             "".join(expected_data[2]), "".join(expected_data[3]))
        self.assertEqual(contents, response.content)

    def test_login_required_for_home_get(self):
        url = '/extract/country/%d/version/%d/'%(self.country.id, 2)
        self.assert_login_required(url)

