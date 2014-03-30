########################################################################################################
# SECTION: School Based Immunization
########################################################################################################
from questionnaire.models import QuestionGroupOrder, QuestionOption, QuestionGroup, Question, SubSection, Section, Questionnaire

questionnaire = Questionnaire.objects.get(name="JRF 2013 Core English", description="From dropbox as given by Rouslan")

section_2 = Section.objects.create(title="School Based Immunization", order=3,
                                    questionnaire=questionnaire, name="School Imm. Delivery", description="""Please complete this section if in your country
routine immunization is given to school-aged children using the school as a venue. For the purpose of this section,
please consider as ""routine"" only those doses that are part of the national immunization schedule.
Do not include doses given in campaigns, even if during those campaigns schools were used as vaccination sites.""")
sub_section_3 = SubSection.objects.create(order=1, section=section_2)

question7 = Question.objects.create(text='Are any routine doses of vaccine given to children at school?', UID='C00007', answer_type='MultiChoice')
QuestionOption.objects.create(text="Yes", question=question7)
QuestionOption.objects.create(text="No", question=question7)
QuestionOption.objects.create(text="NR", question=question7)

question_7_group = QuestionGroup.objects.create(subsection=sub_section_3, order=1)
question_7_group.question.add(question7)

QuestionGroupOrder.objects.create(question=question7, question_group=question_7_group, order=1)

question8 = Question.objects.create(text='Vaccine procurement', UID='C00008', answer_type='MultiChoice')
QuestionOption.objects.create(text="Yes", question=question8)
QuestionOption.objects.create(text="No", question=question8)

question9 = Question.objects.create(text='Vaccinators', UID='C00009', answer_type='MultiChoice')
QuestionOption.objects.create(text="Yes", question=question9)
QuestionOption.objects.create(text="No", question=question9)

question10 = Question.objects.create(text='Supervision', UID='C00010', answer_type='MultiChoice')
QuestionOption.objects.create(text="Yes", question=question10)
QuestionOption.objects.create(text="No", question=question10)

question11 = Question.objects.create(text='Planing', UID='C00011', answer_type='MultiChoice')
QuestionOption.objects.create(text="Yes", question=question11)
QuestionOption.objects.create(text="No", question=question11)

question_8_11__group = QuestionGroup.objects.create(subsection=sub_section_3, order=2, name="Which "
"activities is the EPI Program responsible for (and not the school staff per se ):")

question_8_11__group.question.add(question8, question9, question10, question11)

QuestionGroupOrder.objects.create(question=question8, question_group=question_8_11__group, order=1)
QuestionGroupOrder.objects.create(question=question9, question_group=question_8_11__group, order=2)
QuestionGroupOrder.objects.create(question=question10, question_group=question_8_11__group, order=3)
QuestionGroupOrder.objects.create(question=question11, question_group=question_8_11__group, order=4)

question12 = Question.objects.create(text='Is this part of a comprehensive school health program that delivers other '
                                          'health intervention also?', UID='C00012', answer_type='MultiChoice')
QuestionOption.objects.create(text="Yes", question=question12)
QuestionOption.objects.create(text="No", question=question12)

question13 = Question.objects.create(text='Which interventions are given in the school health program?', UID='C00013', answer_type='Text')


question_12__13_group = QuestionGroup.objects.create(subsection=sub_section_3, order=3)
question_12__13_group.question.add(question12, question13)

QuestionGroupOrder.objects.create(question=question12, question_group=question_12__13_group, order=1)
QuestionGroupOrder.objects.create(question=question13, question_group=question_12__13_group, order=2)


#################################### next sub
sub_section_4 = SubSection.objects.create(order=2, section=section_2, title="Routine Immunization given at school "
    "(please complete one row  for each grade level or age and vaccine)", description="""
     Please complete the table by using one row for each vaccine and each target group. Examples: if TT
     and MR is given in grade 2 and TT in grade 8, use three rows (TT-grade 2; MR-grade 2; TT-grade 8);
     if TT and MR are given to children aged 8 years, and TT to children aged 14 years, use three rows
      (TT-8 years; MR-8 years; TT-14 years)
     """)

question14 = Question.objects.create(text='Vaccine', UID='C00014', answer_type='Text', is_primary=True)
question15 = Question.objects.create(text='Grade/Level', UID='C00015', answer_type='Number',
instructions="""
"Grade / Level" indicates the class or grade that is targeted for
the vaccine concerned. Complete this cell if children in school are targeted by class or grade,
 regardless of their age. Please use the local gradation system, or use a class grading system of 1 to 12, where class 1
  equals the first year in primary school, class 2 the second year of primary school, etc.  """)

question16 = Question.objects.create(text='Age Group', UID='C00016', answer_type='Number',
instructions="""
"Age group" indicates the age groups that are targeted for the vaccine concerned. Complete this cell if children are
 targeted according to their age rather than according to the class they are in.
""")
question17 = Question.objects.create(text='Sex', UID='C00017', answer_type='MultiChoice')
QuestionOption.objects.create(text="Female", question=question17)
QuestionOption.objects.create(text="Male", question=question17)
QuestionOption.objects.create(text="Both", question=question17)

question18 = Question.objects.create(text='Geographic Area', UID='C00018', answer_type='MultiChoice')
QuestionOption.objects.create(text="Subnational", question=question18)
QuestionOption.objects.create(text="National", question=question18)

question19 = Question.objects.create(text='Number in target group', UID='C00019', answer_type='Number',
instructions="""
"Number targeted" is the number of children targeted through the school-based immunization for each dose.
If school-based immunization is not given in all the areas of the country, the target is the number of children
 in the areas where school-based immunization is being implemented
""")

question20 = Question.objects.create(text='Number of doses administered at school', UID='C00020', answer_type='Number',
instructions="""
"Number vaccinated in school": the number for children who received this dose in the areas where school-based
immunization is being implemented.
 """)

question21 = Question.objects.create(text='Other interventions given with the vaccine', UID='C00021',
                                     answer_type='Text',
instructions="""
"Other intervention given with the vaccine":  Mention any other intervention
(e.g. growth monitoring, antihelmintics,...) that is given at the same time as the vaccination contact """)

question22 = Question.objects.create(text='Does recorded on immunization or child death card', UID='C00022',
                                     answer_type='MultiChoice')
QuestionOption.objects.create(text="Yes", question=question22)
QuestionOption.objects.create(text="No", question=question22)

question_14_22_group = QuestionGroup.objects.create(subsection=sub_section_4, order=1, allow_multiples=True, grid=True)
question_14_22_group.question.add(question14, question15, question16, question17, question18, question19,
                                   question20, question21, question22)

QuestionGroupOrder.objects.create(question=question14, question_group=question_14_22_group, order=1)
QuestionGroupOrder.objects.create(question=question15, question_group=question_14_22_group, order=2)
QuestionGroupOrder.objects.create(question=question16, question_group=question_14_22_group, order=3)
QuestionGroupOrder.objects.create(question=question17, question_group=question_14_22_group, order=4)
QuestionGroupOrder.objects.create(question=question18, question_group=question_14_22_group, order=5)
QuestionGroupOrder.objects.create(question=question19, question_group=question_14_22_group, order=6)
QuestionGroupOrder.objects.create(question=question20, question_group=question_14_22_group, order=7)
QuestionGroupOrder.objects.create(question=question21, question_group=question_14_22_group, order=8)
QuestionGroupOrder.objects.create(question=question22, question_group=question_14_22_group, order=9)

############################################ GENERATE FIXTURES
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