from urllib import quote
from django.test import Client
from questionnaire.models import Questionnaire, Section, SubSection, Question, QuestionGroup, Organization, Region, Country, NumericalAnswer, Answer, QuestionGroupOrder, AnswerGroup
from questionnaire.tests.base_test import BaseTest


class ExportToTextViewTest(BaseTest):
    def setUp(self):
        self.client = Client()
        self.user, self.country = self.create_user_with_no_permissions()
        self.login_user()

        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English",
                                                          description="From dropbox as given by Rouslan", year=2013)
        self.section_1 = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)",
                                                order=1,
                                                questionnaire=self.questionnaire, name="Reported Cases")

        self.sub_section = SubSection.objects.create(title="Reported cases for the year 2013", order=1,
                                                     section=self.section_1)
        self.question1 = Question.objects.create(text='B. Number of cases tested',
                                                 instructions="Enter the total number of cases for which specimens were collected, and tested in laboratory",
                                                 UID='C00003', answer_type='Number')

        self.question2 = Question.objects.create(text='C. Number of cases positive',
                                                 instructions="Include only those cases found positive for the infectious agent.",
                                                 UID='C00004', answer_type='Number')

        self.parent = QuestionGroup.objects.create(subsection=self.sub_section, order=1)
        self.parent.question.add(self.question1, self.question2)
        self.organisation = Organization.objects.create(name="WHO")
        self.regions = Region.objects.create(name="The Afro", organization=self.organisation)
        self.country = Country.objects.create(name="Uganda", code="UGX")
        self.regions.countries.add(self.country)

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
        form_data = {'questionnaire': self.questionnaire.id}
        file_name = "%s-%s.txt" % (self.questionnaire.name, self.questionnaire.year)
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