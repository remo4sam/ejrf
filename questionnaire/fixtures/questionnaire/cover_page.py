from questionnaire.models import Questionnaire, Section, SubSection, Question, QuestionGroup, QuestionGroupOrder
from django.core import serializers

questionnaire = Questionnaire.objects.get(name="JRF 2013 Core English", description="From dropbox as given by Rouslan")

section_1 = Section.objects.create(order=0,
                        title="WHO/UNICEF Joint Reporting Form on Immunization for the Period January-December, 2013",
                        description="""If a question is not relevant, enter "NR" (not relevant).<br/>
                                       If no data are available, enter "ND" (no data).<br/>
                                        If the number of cases is zero, enter 0.""",
                        questionnaire=questionnaire, name="Cover page")
sub_section = SubSection.objects.create(order=1, section=section_1)
question1 = Question.objects.create(text='Name of person in Ministry of Health responsible for completing this form',
                                    UID='C00023', answer_type='Text', export_label='Name of person in Ministry of Health responsible for completing this form', is_required=True, instructions="""
List the name of the person responsible for submitting the completed form.
Since multiple departments in the Ministry of Health may have relevant data,
 this person should liaise with other departments to ensure that the form
 contains the most accurate and complete data possible. For example,
 information on Vitamin A may come from the nutrition department.""")
question2 = Question.objects.create(text='Position/title', UID='C00024', export_label='Submitter position/title',  is_required=True, answer_type='Text',)
question3 = Question.objects.create(text='Email address', UID='C00025', answer_type='Text', export_label='Submitter email address',  is_required=True,)
question4 = Question.objects.create(text='Name of UNICEF contact', UID='C00026', export_label='Name of UNICEF contact', answer_type='Text',)
question5 = Question.objects.create(text='Email address of UNICEF contact', UID='C00027', export_label='UNICEF contact email address',  answer_type='Text',)
question6 = Question.objects.create(text='Name of WHO contact', UID='C00028', export_label='Name of WHO contact' , answer_type='Text',)
question7 = Question.objects.create(text='Email address of WHO contact', UID='C00029', export_label='WHO contact email address', answer_type='Text',)
question8 = Question.objects.create(text='Total number of districts in the country', export_label='Total number of districts in the country.', UID='C00030', answer_type='Number',
                                    instructions="""
                                    A district is defined as the third administrative level (nation is the first, province is the second).
                                    """)

parent = QuestionGroup.objects.create(subsection=sub_section, order=1)
parent.question.add(question1, question2, question3, question4, question5, question6, question7, question8)

QuestionGroupOrder.objects.create(question=question1, question_group=parent, order=1)
QuestionGroupOrder.objects.create(question=question2, question_group=parent, order=2)
QuestionGroupOrder.objects.create(question=question3, question_group=parent, order=3)
QuestionGroupOrder.objects.create(question=question4, question_group=parent, order=4)
QuestionGroupOrder.objects.create(question=question5, question_group=parent, order=5)
QuestionGroupOrder.objects.create(question=question6, question_group=parent, order=6)
QuestionGroupOrder.objects.create(question=question7, question_group=parent, order=7)
QuestionGroupOrder.objects.create(question=question8, question_group=parent, order=8)


# data = serializers.serialize("json", [section_1, sub_section, parent])
# print data
#
# data = serializers.serialize("json", parent.question.all())
# print data
#
# data = serializers.serialize("json", parent.orders.all())
# print data
#
