from django.core import serializers
from questionnaire.models import Questionnaire, Section, SubSection, Question, QuestionGroup, QuestionOption, QuestionGroupOrder

questionnaire = Questionnaire.objects.get(name="JRF 2013 Core English", description="From dropbox as given by Rouslan")

section_1 = Section.objects.create(order=8, questionnaire=questionnaire, name="Supplementary",
                                   title="Supplementary Activities",
                                   description="Please record any additional immunization and nutritional interventions, including Vitamin A and iron supplementation, deworming, and the distribution of insecticide treated bednets.")

sub_section = SubSection.objects.create(order=1, section=section_1, title="Conducted during 2013")

question1 = Question.objects.create(text="Vaccine/supplement", UID='C00129', answer_type='Text', export_label='Vaccine or supplement name')
question2 = Question.objects.create(text="Round and type of activity", export_label='Round and type of activity',  UID='C00130', answer_type='Text',
instructions="Record the name of the activity (for example, NIDs, micronutrition day, child health day, or vaccination week) and the number of the round (for example, first, second or third). If an activity involved more than one vaccine or supplement, use multiple lines to describe it, placing each vaccine or supplement on a separate line.")
question3 = Question.objects.create(text="Date", UID='C00131', answer_type='Date', export_label='Date')
question4 = Question.objects.create(text="Geographic Area", UID='C00132', answer_type='MultiChoice', export_label='Geographic Area')
question5 = Question.objects.create(text="Target population", UID='C00133', answer_type='Text',
                                    export_label='Target population (age group)',
instructions="If children are targeted, specify the age of the target group. If women are targeted, specify the age and/or pregnancy status of the target group, for example, women of childbearing age or pregnant women.")
question6 = Question.objects.create(text="Estimated number in target population", export_label='Estimated number in target population', UID='C00134', answer_type='Number')
question7 = Question.objects.create(text="Total number of persons vaccinated or supplemented",
                                    export_label='Total number of persons vaccinated/supplemented', UID='C00135', answer_type='Number')
question8 = Question.objects.create(text="Coverage (%)", UID='C00136', answer_type='Number', export_label='Coverage (%)',
instructions="Enter the official coverage estimate for the vaccine or supplement (including measles, yellow fever, meningitis, and polio vaccines and Vitamin A). Do NOT complete for tetanus vaccine. These estimates can come from a coverage survey and thus may differ from the administrative calculation.")

group = QuestionGroup.objects.create(subsection=sub_section, order=1, allow_multiples=True,
instructions="Record all supplementary activities related to immunization and nutritional supplementation that were conducted at either the national or sub-national levels in 2013. These could include activities related to polio, yellow fever, measles, rubella, influenza, meningitis, and tetanus toxoid vaccines; vitamin A and iron supplements; deworming; and the distribution of insecticide treated bednets (ITNs).")
group.question.add(question1, question2, question3, question4, question5, question6, question7, question8)

question11 = Question.objects.create(text="TT1", UID='C00137', answer_type='Number', export_label='Number of persons vaccinated TT1')
question12 = Question.objects.create(text="TT2", UID='C00138', answer_type='Number', export_label='Number of persons vaccinated TT2')
question13 = Question.objects.create(text="TT3", UID='C00139', answer_type='Number', export_label='Number of persons vaccinated TT3')
question14 = Question.objects.create(text="TT4 or more", UID='C00140', answer_type='Number', export_label='Number of persons vaccinated TT4 or more')

subgroup = QuestionGroup.objects.create(subsection=sub_section, parent = group,
name="Number of persons vaccinated for tetanus",
instructions="Columns must add up to Total Number of Persons Vaccinated")
subgroup.question.add(question11, question12, question13, question14)

QuestionOption.objects.create(question=question4, text="National")
QuestionOption.objects.create(question=question4, text="Subnational")

QuestionGroupOrder.objects.create(question=question1, question_group=group, order=1)
QuestionGroupOrder.objects.create(question=question2, question_group=group, order=2)
QuestionGroupOrder.objects.create(question=question3, question_group=group, order=3)
QuestionGroupOrder.objects.create(question=question4, question_group=group, order=4)
QuestionGroupOrder.objects.create(question=question5, question_group=group, order=5)
QuestionGroupOrder.objects.create(question=question6, question_group=group, order=6)
QuestionGroupOrder.objects.create(question=question7, question_group=group, order=7)
QuestionGroupOrder.objects.create(question=question8, question_group=group, order=8)
QuestionGroupOrder.objects.create(question=question11, question_group=group, order=9)
QuestionGroupOrder.objects.create(question=question12, question_group=group, order=10)
QuestionGroupOrder.objects.create(question=question13, question_group=group, order=11)
QuestionGroupOrder.objects.create(question=question14, question_group=group, order=12)


############################################################################################


sub_section2 = SubSection.objects.create(order=2, section=section_1, title="Planned for 2014-2015")

group2 = QuestionGroup.objects.create(subsection=sub_section2, order=1, allow_multiples=True,
instructions="Record any supplementary activities related to immunization and nutritional supplementation, at either the national or sub-national levels, that are planned for 2014 and 2015. These could include activities related to polio, yellow fever, measles, rubella, influenza, meningitis, and tetanus toxoid vaccines; vitamin A and iron supplements; deworming; and the distribution of insecticide-treated bednets (ITNs).")
group2.question.add(question1, question2, question3, question4, question5, question6)

QuestionGroupOrder.objects.create(question=question1, question_group=group2, order=1)
QuestionGroupOrder.objects.create(question=question2, question_group=group2, order=2)
QuestionGroupOrder.objects.create(question=question3, question_group=group2, order=3)
QuestionGroupOrder.objects.create(question=question4, question_group=group2, order=4)
QuestionGroupOrder.objects.create(question=question5, question_group=group2, order=5)
QuestionGroupOrder.objects.create(question=question6, question_group=group2, order=6)
#
# ############################################ GENERATE FIXTURES
# questionnaires = Questionnaire.objects.all()
# sections = Section.objects.all()
# subsections = SubSection.objects.all()
# questions = Question.objects.all()
# question_groups = QuestionGroup.objects.all()
# options = QuestionOption.objects.all()
# orders = QuestionGroupOrder.objects.all()
#

# data = serializers.serialize("json", [questionnaires])
# print data

# data = serializers.serialize("json", [sections])
# print data

# data = serializers.serialize("json", [subsections])
# print data
#
# data = serializers.serialize("json", [questions])
# print data
#
# data = serializers.serialize("json", [question_groups])
# print data
#
# data = serializers.serialize("json", [options, orders])
# print data


# ./manage.py dumpdata  questionnaire questionnaire.Questionnaire questionnaire.Section questionnaire.Subsection questionnaire.Question questionnaire.QuestionGroup questionnaire.QuestionOption questionnaire.QuestionGroupOrder --settings=eJRF.testsettings > haha.json