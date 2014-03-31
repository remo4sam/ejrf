from django.core import serializers
from questionnaire.models import Questionnaire, Section, SubSection, Question, QuestionGroup, QuestionOption, QuestionGroupOrder

questionnaire = Questionnaire.objects.get(name="JRF 2013 Core English", description="From dropbox as given by Rouslan")

section_1 = Section.objects.create(order=6, questionnaire=questionnaire, name="Official Estimates",
                                   title="Official Country Estimates of Immunization Coverage for the Year 2013",
                                   description="Please complete separately for each vaccine, even if they are given in combination (e.g., if Pentavalent vaccine DTP-HepB-Hib is used, fill in the data for DTP3, HepB3 and Hib3)")

sub_section = SubSection.objects.create(order=1, section=section_1, title=" ")

question1 = Question.objects.create(text="Vaccine/Supplement", UID='C00071', export_label='Vaccine or supplement name',
                                    answer_type='MultiChoice', is_primary=True)

QuestionOption.objects.create(text="BCG", question=question1)
QuestionOption.objects.create(text="HepB, birth dose", question=question1)
QuestionOption.objects.create(text="DTP1", question=question1)
QuestionOption.objects.create(text="DTP3", question=question1)
QuestionOption.objects.create(text="Polio3", question=question1)
QuestionOption.objects.create(text="HepB3", question=question1)
QuestionOption.objects.create(text="Hib3", question=question1)
QuestionOption.objects.create(text="Pneumococcal conjugate vaccine 1st dose", question=question1)
QuestionOption.objects.create(text="Pneumococcal conjugate vaccine 2nd dose", question=question1)
QuestionOption.objects.create(text="Pneumococcal conjugate vaccine 3rd dose", question=question1)
QuestionOption.objects.create(text="Rotavirus 1st dose", question=question1)
QuestionOption.objects.create(text="Rotavirus last dose (2nd or 3rd depending on schedule)", question=question1)
QuestionOption.objects.create(text="MCV1 (measles-containing vaccine, 1st dose)", question=question1)
QuestionOption.objects.create(text="Rubella 1 (rubella-containing vaccine)", question=question1)
QuestionOption.objects.create(text="MCV2 (measles-containing vaccine, 2nd dose)", question=question1)
QuestionOption.objects.create(text="Yellow fever vaccine", question=question1)
QuestionOption.objects.create(text="Japanese encephalitis vaccine", question=question1)
QuestionOption.objects.create(text="Vitamin A, 1st dose", question=question1)
QuestionOption.objects.create(text="Vitamin A, 1st dose", question=question1)
QuestionOption.objects.create(text="Tetanus toxoid-containing vaccine (TT2+) for pregnant women", question=question1)

question2 = Question.objects.create(text="Official coverage estimates (percent coverage)",
                                    UID='C00072', answer_type='Text')

parent1 = QuestionGroup.objects.create(subsection=sub_section, order=1, display_all=True, grid=True)
parent1.question.add(question2, question1)
QuestionGroupOrder.objects.create(question=question1, question_group=parent1, order=1)
QuestionGroupOrder.objects.create(question=question2, question_group=parent1, order=2)


sub_section1 = SubSection.objects.create(order=2, section=section_1, title=" ")
question_1 = Question.objects.create(text="Please explain why these are your official estimates and where they come from",
                                      export_label='Explanatory comments on official coverage estimates',
                                     UID='C00073', answer_type='Text', instructions="")

parent2 = QuestionGroup.objects.create(subsection=sub_section1, order=1)
parent2.question.add(question_1)
QuestionGroupOrder.objects.create(question=question_1, question_group=parent2, order=1)

# data = serializers.serialize("json", [section_1, sub_section, sub_section1])
# print data
#
# data = serializers.serialize("json", [parent1, parent2])
# print data
#
# data = serializers.serialize("json", parent1.question.all())
# print data
# data = serializers.serialize("json", parent1.orders.all())
# print data
#
# data = serializers.serialize("json", parent2.orders.all())
# print data
#
# data = serializers.serialize("json", parent2.question.all())
# print data
#
