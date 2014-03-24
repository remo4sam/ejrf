from django.core import serializers
from questionnaire.models import Questionnaire, Section, SubSection, Question, QuestionGroup, QuestionOption, QuestionGroupOrder

questionnaire = Questionnaire.objects.get(name="JRF 2013 Core English", description="From dropbox as given by Rouslan")

section_1 = Section.objects.create(order=4, questionnaire=questionnaire, name="Routine Coverage",
                                   title="Immunization and Vitamin A Coverage <br/> National Administrative Coverage for the Year 2013")

sub_section = SubSection.objects.create(order=1, section=section_1, title="Administrative coverage")

question1 = Question.objects.create(text="Vaccine/Supplement", is_primary=True,
                                    UID='C00048', answer_type='MultiChoice',
                                    instructions="Please complete separately for each vaccine,  even if they are given in combination (e.g., if Pentavalent vaccine DTP-HepB-Hib is used, fill in the data for DTP3, HepB3 and Hib3)")

QuestionOption.objects.create(text="BCG", question=question1)
QuestionOption.objects.create(text="HepB, birth dose (given within 24 hours of birth)", question=question1,
instructions="Provide ONLY hepatitis B vaccine doses given within 24 hours of birth.  If time of birth is unknown, please provide doses of hepatitis B vaccine given within first day of life.  (For example, if the infant is born on day 0, include all HepB does given on days 0 and 1.)  This indicator is NOT equivalent to HepB1")

QuestionOption.objects.create(text="DTP1", question=question1)
QuestionOption.objects.create(text="DTP3", question=question1)
QuestionOption.objects.create(text="Polio3 (OPV or IPV)", question=question1,
instructions="This refers to the third dose of polio vaccine, excluding polio 0 (zero), if such a dose is included in the national schedule.")

QuestionOption.objects.create(text="HepB3", question=question1,
instructions="""In countries using monovalent vaccine for all doses, this refers to the third dose of hepatitis B vaccine, including the birth dose, if such a dose is included in the national schedule.<br/>
In countries that are using monovalent vaccine for the birth dose and combination vaccine for the subsequent doses, HepB3 will refer to the third dose of the combination vaccine in addition to the birth dose.""")

QuestionOption.objects.create(text="Hib3", question=question1)
QuestionOption.objects.create(text="Pneumococcal conjugate vaccine 1st dose", question=question1)
QuestionOption.objects.create(text="Pneumococcal conjugate vaccine 2nd dose", question=question1)
QuestionOption.objects.create(text="Pneumococcal conjugate vaccine 3rd dose", question=question1)
QuestionOption.objects.create(text="Rotavirus 1st dose", question=question1)
QuestionOption.objects.create(text="Rotavirus last dose (2nd or 3rd depending on schedule)", question=question1)
QuestionOption.objects.create(text="MCV1 (measles-containing vaccine, 1st dose)", question=question1,
instructions="Measles-containing vaccine (MCV) includes measles vaccine, measles-rubella vaccine, measles-mumps-rubella vaccine, etc. Fill in the rows for both MCV and rubella vaccines even if they were given in combination.")

QuestionOption.objects.create(text="Rubella 1 (rubella-containing vaccine)", question=question1,
instructions="Measles-containing vaccine (MCV) includes measles vaccine, measles-rubella vaccine, measles-mumps-rubella vaccine, etc. Fill in the rows for both MCV and rubella vaccines even if they were given in combination.")

QuestionOption.objects.create(text="MCV2 (measles-containing vaccine, 2nd dose)", question=question1,
instructions="Measles-containing vaccine (MCV) includes measles vaccine, measles-rubella vaccine, measles-mumps-rubella vaccine, etc. Fill in the rows for both MCV and rubella vaccines even if they were given in combination.")

QuestionOption.objects.create(text="Vitamin A, 1st dose", question=question1)
QuestionOption.objects.create(text="Japanese encephalitis vaccine", question=question1)
QuestionOption.objects.create(text="Tetanus toxoid-containing vaccine (TT2+) ", question=question1)
QuestionOption.objects.create(text="Protection at birth (PAB) against neonatal tetanus", question=question1,
instructions="This refers to children who are protected at birth (PAB) against neonatal tetanus by their mother's TT status; this information is collected during the DTP1 visit - a child is deemed protected if the mother has received 2 doses of TT in the last pregnancy or at-least 3 doses of TT in previous years. If the country does not calculate PAB, leave the cells blank.")


question2 = Question.objects.create(text="Description of the denominator used in coverage calculation",
                                    UID='C00049', answer_type='MultiChoice')

QuestionOption.objects.create(text="live birth", question=question2)
QuestionOption.objects.create(text="surviving infants", question=question2)
QuestionOption.objects.create(text="less than 59 months", question=question2)
QuestionOption.objects.create(text="12 - 59 months", question=question2)
QuestionOption.objects.create(text="6 - 59 months", question=question2)
QuestionOption.objects.create(text="pregnant women", question=question2,
instructions="The number of live births can be used as a proxy for the total number of pregnant women.")

question3 = Question.objects.create(text="Number in target group(denominator)",
                                    UID='C00050', answer_type='Number', )
question4 = Question.objects.create(text="Number of doses administered through routine services (numerator)",
                                    UID='C00051', answer_type='Number')
question5 = Question.objects.create(text="Percent coverage (=C/B*100)", UID='C00052', answer_type='Number')

parent1 = QuestionGroup.objects.create(subsection=sub_section, order=1, allow_multiples=True, grid=True)
parent1.question.add(question1, question2, question3, question3, question4, question5)

QuestionGroupOrder.objects.create(question=question1, question_group=parent1, order=1)
QuestionGroupOrder.objects.create(question=question2, question_group=parent1, order=2)
QuestionGroupOrder.objects.create(question=question3, question_group=parent1, order=3)
QuestionGroupOrder.objects.create(question=question4, question_group=parent1, order=4)
QuestionGroupOrder.objects.create(question=question5, question_group=parent1, order=5)

sub_section2 = SubSection.objects.create(order=2, section=section_1, title="Accuracy of administrative coverage",
                                         description="Administrative coverage estimates can be biased by inaccurate numerators and/or denominators. Use this space to describe any factors limiting the accuracy of the coverage estimates entered in the table above. Some common problems are listed here. Numerators may be underestimated because of incomplete reporting from reporting units or the exclusion of other vaccinating sources, such as the private sector and NGOs; or overestimated because of over-reporting from reporting units, for example, when other target groups are included. Denominators may have problems arising from population movements, inaccurate census estimations or projections, or multiple sources of data.")

question21 = Question.objects.create(text="Describe any factors limiting the accuracy of the numerator: ",
                                     UID='C00053', answer_type='Text')
question22 = Question.objects.create(text="Describe any factors limiting the accuracy of the denominator: (denominator = number in target group)",
                                     UID='C00054', answer_type='Text')

parent2 = QuestionGroup.objects.create(subsection=sub_section2, order=1)
parent2.question.add(question21)

QuestionGroupOrder.objects.create(question=question21, question_group=parent2, order=1)

parent3 = QuestionGroup.objects.create(subsection=sub_section2, order=2)
parent3.question.add(question22)
QuestionGroupOrder.objects.create(question=question22, question_group=parent3, order=1)

sub_section3 = SubSection.objects.create(order=3, section=section_1, title="Completeness of district level reporting",
                                         description="This table collects information about the completeness of district reporting, i.e., the main reporting system which produced the numbers in the previous table on vaccine coverage. The number of expected reports is equal to the number of districts multiplied by the number of reporting periods in the year")

question31 = Question.objects.create(text="Total number of district reports expected at the national level from all districts across repording periods in 2013 (e.g., # districts x 12 months)",
                                     UID='C00055', answer_type='Number')

question32 = Question.objects.create(text="Total number of district reports actually received at the national level from all districts across reporting periods in 2013",
                                     UID='C00056', answer_type='Number')

parent4 = QuestionGroup.objects.create(subsection=sub_section3, order=1)
parent4.question.add(question31)
QuestionGroupOrder.objects.create(question=question31, question_group=parent4, order=1)

parent5 = QuestionGroup.objects.create(subsection=sub_section3, order=2)
parent5.question.add(question32)
QuestionGroupOrder.objects.create(question=question32, question_group=parent5, order=1)

sub_section4 = SubSection.objects.create(order=4, section=section_1, title="HPV Vaccine Doses administered: 2013",
                                         description="Report the number of HPV vaccinations given to females by their age at time of administration for each of the three recommended doses of HPV vaccine. If age is unknown but can be estimated, report for the estimated age. For example, if vaccination is offered exclusively to girls in the 6th school form and most girls in the 6th school form are eleven years of age, vaccinations by dose may be reported as vaccinations for girls eleven years of age.")

question41 = Question.objects.create(text="Vaccine administered (age in years)", UID='C00057', answer_type='MultiChoice', is_primary=True)
QuestionOption.objects.create(text="9", question=question41)
QuestionOption.objects.create(text="10", question=question41)
QuestionOption.objects.create(text="11", question=question41)
QuestionOption.objects.create(text="12", question=question41)
QuestionOption.objects.create(text="13", question=question41)
QuestionOption.objects.create(text="14", question=question41)
QuestionOption.objects.create(text="15+", question=question41)
QuestionOption.objects.create(text="unknown age", question=question41)

question42 = Question.objects.create(text="1st dose", UID='C00058', answer_type='Number')
question43 = Question.objects.create(text="2d dose", UID='C00059', answer_type='Number')
question44 = Question.objects.create(text="3d dose", UID='C00060', answer_type='Number')

parent7 = QuestionGroup.objects.create(subsection=sub_section4, order=1, allow_multiples=False, grid=True, display_all=True)
parent7.question.add(question41, question42, question43, question44)
QuestionGroupOrder.objects.create(question=question41, question_group=parent7, order=1)
QuestionGroupOrder.objects.create(question=question42, question_group=parent7, order=2)
QuestionGroupOrder.objects.create(question=question43, question_group=parent7, order=3)
QuestionGroupOrder.objects.create(question=question44, question_group=parent7, order=4)

sub_section5 = SubSection.objects.create(order=5, section=section_1, title="Accuracy of reported HPV Vaccine Doses")

question51 = Question.objects.create(text="Describe any factors limiting the accuracy of the administered doses",
                                     UID='C00061', answer_type='Text')
parent8 = QuestionGroup.objects.create(subsection=sub_section5, order=1)
parent8.question.add(question51)
QuestionGroupOrder.objects.create(question=question51, question_group=parent8, order=1)

sub_section6 = SubSection.objects.create(order=6, section=section_1, title="Seasonal Influenza Vaccine Doses Administered",
                                         description="In an updated position paper (2012), WHO recommends that countries considering the initiation or expansion of seasonal influenza vaccination programmes give the highest priority to pregnant women. Additional risk groups to be considered for vaccination, in no particular order of priority, are: children aged 6-59 months; the elderly; individuals with specific chronic medical conditions; and healthcare workers. Report immunization coverage in this table using data collected from vaccination clinics/sites on the number of doses administered for each of the risk groups that are included in the country-specific policy for seasonal influenza vaccination. ")

question61 = Question.objects.create(text="Description of target population", UID='C00062', answer_type='MultiChoice')
QuestionOption.objects.create(text="Children 6-23 months", question=question61)
QuestionOption.objects.create(text="Children >=24 months up to 9 years", question=question61)
QuestionOption.objects.create(text="Elderly (please specify minimum age under explanatory comments)", question=question61)
QuestionOption.objects.create(text="Pregnant women", question=question61)
QuestionOption.objects.create(text="Health care workers", question=question61)
QuestionOption.objects.create(text="Persons with chronic diseases ", question=question61)
#instruction = (e.g. respiratory, cardiac, liver and renal diseases; neurodevelopmental, immunological and haematological disorders, diabetes; obesity etc.)
QuestionOption.objects.create(text="Others)", question=question61)
#instruction = (may include various other groups: poultry workers, subnational levels, government officials, adults, etc

question62 = Question.objects.create(text="Number in target group (denominator)", UID='C00063', answer_type='Number')
question63 = Question.objects.create(text="Number of doses administered through routine services (numerator)", UID='C00064', answer_type='Number')
question64 = Question.objects.create(text="Percent coverage (=C/B*100)", UID='C00065', answer_type='Number')

parent6 = QuestionGroup.objects.create(subsection=sub_section6, order=1, allow_multiples=True)
parent6.question.add(question61, question62, question63, question64)
QuestionGroupOrder.objects.create(question=question61, question_group=parent6, order=1)
QuestionGroupOrder.objects.create(question=question62, question_group=parent6, order=2)
QuestionGroupOrder.objects.create(question=question63, question_group=parent6, order=3)
QuestionGroupOrder.objects.create(question=question64, question_group=parent6, order=4)


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