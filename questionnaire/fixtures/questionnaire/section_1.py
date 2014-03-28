from questionnaire.models import Questionnaire, Section, SubSection, Question, QuestionGroup, QuestionOption, QuestionGroupOrder
from django.core import serializers

Questionnaire.objects.all().delete()
Section.objects.all().delete()
SubSection.objects.all().delete()
Question.objects.all().delete()
QuestionGroup.objects.all().delete()
QuestionOption.objects.all().delete()
QuestionGroupOrder.objects.all().delete()

questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English",
                                             description="From dropbox as given by Rouslan",
                                             year=2013, status=Questionnaire.PUBLISHED)

########################################################################################################
# SECTION: Reported Cases of Selected Vaccine Preventable Diseases (VPDs)
########################################################################################################
section_1 = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)", order=1,
                                   questionnaire=questionnaire, name="Reported Cases")
sub_section = SubSection.objects.create(title="Reported cases for the year 2013", order=1, section=section_1)

question1 = Question.objects.create(text='Disease', UID='C00001', answer_type='MultiChoice', is_primary=True)
question2 = Question.objects.create(text='Total Cases', export_label='Total number of cases',
instructions="""<strong>Column A</strong> refers only to <strong>CONFIRMED</strong> cases, including those confirmed clinically, epidemiologically, or by laboratory investigation.&nbsp;<br />
<br />
<strong>Clinically-confirmed case:</strong> a case that meets the clinical case definition of the country<br />
<br />
<strong>Epidemiologically-confirmed case: </strong>a case that meets the clinical case definition and is linked epidemiologically to a laboratory-confirmed case<br />
<br />
<strong>Laboratory-confirmed case:</strong> a case that meets the clinical case definition and is confirmed by laboratory investigation<br />
<br />
Cases that have been <strong>discarded</strong> following laboratory investigation should <strong>NOT</strong> be included in these columns.
""",
UID='C00002', answer_type='Number')

question3 = Question.objects.create(text='Number of cases tested', export_label='Number of cases tested',
                                    instructions="Enter the total number of cases for which specimens were collected, and tested in laboratory",
                                    UID='C00003', answer_type='Number')

question4 = Question.objects.create(text='Number of cases positive', export_label='Number of cases positive',
                                    instructions="Include only those cases found positive for the infectious agent.",
                                    UID='C00004', answer_type='Number')

parent = QuestionGroup.objects.create(subsection=sub_section, order=1, allow_multiples=False, grid=True, display_all=True)
parent.question.add(question1, question2)

sub_group = QuestionGroup.objects.create(subsection=sub_section, parent=parent, name="Laboratory Investigation")
sub_group.question.add(question3, question4)

QuestionOption.objects.create(text="Diphteria", question=question1)
QuestionOption.objects.create(text="Measles", question=question1)
QuestionOption.objects.create(text="Neonatal tetanus (NT)", question=question1)
QuestionOption.objects.create(text="Total tetanus (all tetanus including NT)", question=question1)
QuestionOption.objects.create(text="Pertussis", question=question1)
QuestionOption.objects.create(text="Yellow fever", question=question1)
QuestionOption.objects.create(text="Japanese encephalitis", question=question1)
QuestionOption.objects.create(text="Mumps", question=question1)
QuestionOption.objects.create(text="Rubella", question=question1)
QuestionOption.objects.create(text="Congenital rubella syndrome", question=question1)

sub_section_2 = SubSection.objects.create(title="Presence of surveillance systems", order=2, section=section_1)
question5 = Question.objects.create(text="""Is there a surveillance system in place for invasive bacterial diseases (for example bacterial meningitis,
sepsis or bacteremic pneumonia), in which suspected cases are confirmed by laboratory and surveillance data could provide information to allow evaluation
of the impact of vaccination against Hib and/or Pneumococcus?""", export_label='Is there a surveillance system in place for invasive bacterial diseases (for example bacterial meningitis, sepsis or bacteremic pneumonia)',
                                      UID='C00005',
                                      answer_type='MultiChoice')
question_5_group = QuestionGroup.objects.create(subsection=sub_section_2, order=1)
question_5_group.question.add(question5)

QuestionOption.objects.create(text="Yes", question=question5)
QuestionOption.objects.create(text="No", question=question5)
QuestionOption.objects.create(text="NR", question=question5)


question6 = Question.objects.create(text="""Is there a surveillance system in place for rotavirus diarrhoea, in which suspected cases are confirmed
 by laboratory and surveillance data could provide information to allow evaluation of the impact of vaccination against rotavirus?""", export_label='Is there a surveillance system in place for rotavirus diarrhoea, in which suspected cases are confirmed by laboratory and surveillance data',
                                    UID='C00006', answer_type='MultiChoice')

question_6_group = QuestionGroup.objects.create(subsection=sub_section_2, order=2)
question_6_group.question.add(question6)

QuestionOption.objects.create(text="Yes", question=question6)
QuestionOption.objects.create(text="No", question=question6)
QuestionOption.objects.create(text="NR", question=question6)

QuestionGroupOrder.objects.create(question=question1, question_group=parent, order=1)
QuestionGroupOrder.objects.create(question=question2, question_group=parent, order=2)
QuestionGroupOrder.objects.create(question=question3, question_group=parent, order=3)
QuestionGroupOrder.objects.create(question=question4, question_group=parent, order=4)
QuestionGroupOrder.objects.create(question=question5, question_group=question_5_group, order=1)
QuestionGroupOrder.objects.create(question=question6, question_group=question_6_group, order=1)

########################################### GENERATE FIXTURES
questionnaires = Questionnaire.objects.all()
sections = Section.objects.all()
subsections = SubSection.objects.all()
questions = Question.objects.all()
question_groups = QuestionGroup.objects.all()
options = QuestionOption.objects.all()
orders = QuestionGroupOrder.objects.all()

# data = serializers.serialize("json", [questionnaires])
# print data
#
# data = serializers.serialize("json", [sections])
# print data
#
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