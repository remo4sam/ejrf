from django.core import serializers
from questionnaire.models import Questionnaire, Section, SubSection, Question, QuestionGroup, QuestionOption, QuestionGroupOrder

questionnaire = Questionnaire.objects.get(name="JRF 2013 Core English", description="From dropbox as given by Rouslan")

section_1 = Section.objects.create(order=5, questionnaire=questionnaire, name="Coverage Surveys",
                                   title="Immunization and Vitamin A Coverage")

sub_section = SubSection.objects.create(order=1, section=section_1, title="Conducted in 2011-2013")

question1 = Question.objects.create(text="Year of most recent survey", UID='C00066', answer_type='MultiChoice',export_label='When was the most recent survey conducted?',
                                    instructions="If a coverage survey or other surveys with immunization modules have been conducted from 2011 onwards, indicate whenit took place (if more than one survey took place during this time period, select the latest most recent one)?")

QuestionOption.objects.create(text="2011", question=question1)
QuestionOption.objects.create(text="2012", question=question1)
QuestionOption.objects.create(text="2013", question=question1)

question2 = Question.objects.create(text="Full title of survey in the language of the original report", export_label='Full title of survey in the language of the original report',
                                    UID='C00067', answer_type='Text')
question3 = Question.objects.create(text="Full title of survey in English", UID='C00068', answer_type='Text', export_label='Full title of survey in English' )

parent1 = QuestionGroup.objects.create(subsection=sub_section, order=1)
parent1.question.add(question3, question2, question1)
QuestionGroupOrder.objects.create(question=question1, question_group=parent1, order=1)
QuestionGroupOrder.objects.create(question=question2, question_group=parent1, order=2)
QuestionGroupOrder.objects.create(question=question3, question_group=parent1, order=3)


sub_section1 = SubSection.objects.create(order=2, section=section_1, title="Planned for 2014-2015")
question_1 = Question.objects.create(text="Is a coverage survey planned for the next 24 months?", UID='C00069',
                                     export_label='Is a coverage survey planned for the next 24 months?',
                                     answer_type='MultiChoice', instructions="")

QuestionOption.objects.create(text="Yes", question=question_1)
QuestionOption.objects.create(text="No", question=question_1)

question_2 = Question.objects.create(text="What type of survey is planned? (e.g., MICS, DHS, EPI or CES)",
                                     export_label='What type of survey is planned? (e.g., MICS, DHS, EPI or CES)',
                                     UID='C00070', answer_type='Text')

parent2 = QuestionGroup.objects.create(subsection=sub_section1, order=1)
parent2.question.add(question_1, question_2)
QuestionGroupOrder.objects.create(question=question_1, question_group=parent2, order=1)
QuestionGroupOrder.objects.create(question=question_2, question_group=parent2, order=2)


# ############################################ GENERATE FIXTURES
# questionnaires = Questionnaire.objects.all()
# sections = Section.objects.all()
# subsections = SubSection.objects.all()
# questions = Question.objects.all()
# question_groups = QuestionGroup.objects.all()
# options = QuestionOption.objects.all()
# orders = QuestionGroupOrder.objects.all()

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