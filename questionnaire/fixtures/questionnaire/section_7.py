from django.core import serializers
from questionnaire.models import Questionnaire, Section, SubSection, Question, QuestionGroup, QuestionOption, QuestionGroupOrder

questionnaire = Questionnaire.objects.get(name="JRF 2013 Core English", description="From dropbox as given by Rouslan")

section_1 = Section.objects.create(order=7, questionnaire=questionnaire, name="Indicators",
                                   title="Immunization System Indicators")

sub_section = SubSection.objects.create(order=1, section=section_1, title="Planning and management")

question1 = Question.objects.create(text="Does the country have a  multi-year plan (MYP) for immunization?",
                                    UID='C00074', answer_type='MultiChoice')

QuestionOption.objects.create(text="Yes", question=question1)
QuestionOption.objects.create(text="No", question=question1)
QuestionOption.objects.create(text="NR", question=question1)

question2 = Question.objects.create(text="If yes, what years does the MYP cover?", UID='C00075', answer_type='Text')


question3 = Question.objects.create(text="Did the country have an annual workplan for immunization activities in 2013?",
                                    UID='C00076', answer_type='MultiChoice')
QuestionOption.objects.create(text="Yes", question=question3)
QuestionOption.objects.create(text="No", question=question3)
QuestionOption.objects.create(text="NR", question=question3)


question4 = Question.objects.create(text="Number of districts with updated micro-plans to raise immunization coverage",
                                    UID='C00077', answer_type='Text')

parent1 = QuestionGroup.objects.create(subsection=sub_section, order=1)
parent1.question.add(question2, question1, question3, question4)
QuestionGroupOrder.objects.create(question=question1, question_group=parent1, order=1)
QuestionGroupOrder.objects.create(question=question2, question_group=parent1, order=2)
QuestionGroupOrder.objects.create(question=question3, question_group=parent1, order=3)
QuestionGroupOrder.objects.create(question=question4, question_group=parent1, order=4)


sub_section1 = SubSection.objects.create(order=2, section=section_1, title="National Immunization Advisory Mechanism")
question_1 = Question.objects.create(text="Did  your country have a standing technical advisory group on immunization in 2013? If no, please skip to next page",
                                     UID='C00078', answer_type='MultiChoice', instructions="")
QuestionOption.objects.create(text="Yes", question=question_1)
QuestionOption.objects.create(text="No", question=question_1)
QuestionOption.objects.create(text="NR", question=question_1)

question_2 = Question.objects.create(text="Does the advisory group have formal written terms of reference?",
                                     UID='C00125', answer_type='MultiChoice')
QuestionOption.objects.create(text="Yes", question=question_2)
QuestionOption.objects.create(text="No", question=question_2)
QuestionOption.objects.create(text="NR", question=question_2)

question_3 = Question.objects.create(text="Are there legislative or administrative basis for the advisory group?",
                                     UID='C00079', answer_type='MultiChoice')
QuestionOption.objects.create(text="Yes", question=question_3)
QuestionOption.objects.create(text="No", question=question_3)
QuestionOption.objects.create(text="NR", question=question_3)


#subgroup
question_4 = Question.objects.create(text="pediatrics", UID='C00080', answer_type='MultiChoice')
QuestionOption.objects.create(text="Yes", question=question_4)
QuestionOption.objects.create(text="No", question=question_4)
QuestionOption.objects.create(text="NR", question=question_4)

question_5 = Question.objects.create(text="public health", UID='C00126', answer_type='MultiChoice')
QuestionOption.objects.create(text="Yes", question=question_5)
QuestionOption.objects.create(text="No", question=question_5)
QuestionOption.objects.create(text="NR", question=question_5)

question_6 = Question.objects.create(text="infectious diseases", UID='C00081', answer_type='MultiChoice')
QuestionOption.objects.create(text="Yes", question=question_6)
QuestionOption.objects.create(text="No", question=question_6)
QuestionOption.objects.create(text="NR", question=question_6)

question_7 = Question.objects.create(text="epidemiology", UID='C00082', answer_type='MultiChoice')
QuestionOption.objects.create(text="Yes", question=question_7)
QuestionOption.objects.create(text="No", question=question_7)
QuestionOption.objects.create(text="NR", question=question_7)

question_8 = Question.objects.create(text="immunology", UID='C00083', answer_type='MultiChoice')
QuestionOption.objects.create(text="Yes", question=question_8)
QuestionOption.objects.create(text="No", question=question_8)
QuestionOption.objects.create(text="NR", question=question_8)

question_9 = Question.objects.create(text="other: please specify under explanatory comments", UID='C00084',
                                     answer_type='MultiChoice')
QuestionOption.objects.create(text="Yes", question=question_9)
QuestionOption.objects.create(text="No", question=question_9)
QuestionOption.objects.create(text="NR", question=question_9)


# *************************************************************
#end of subgroup
#******************************************************************

question_10 = Question.objects.create(text="How many times did the advisory group meet in 2013?", UID='C00085', answer_type='Number',
                                      instructions="Altough groups can have ad hoc meetings when necessary, it is recommended to have meetings at regular intervals on predetermined dates and at least once a year. This ensures that the group remains active and recommendations remain current. And it also facilitates increased attendance rates allowing members to plan the time commitment into their schedules in advance.")

question_11 = Question.objects.create(text="Were the agenda and background documents distributed (at least 1 week) prior to meetings in 2013?", UID='C00086', answer_type='MultiChoice',
                                      instructions="An agenda for each NITAG meeting should be distributed in advance to all members. This allows to properly prepare for the meeting. Ideally, background materials would also be distributed prior to the meetings to provide members with current research available on the topic. The distribution of this material facilitates a well rounded, informed discussion during the meeting, provided the members receive the information within sufficient time prior to the meeting.")
QuestionOption.objects.create(text="Yes", question=question_11)
QuestionOption.objects.create(text="No", question=question_11)
QuestionOption.objects.create(text="NR", question=question_11)

question_12 = Question.objects.create(text="Are members of the advisory group required to disclose conflict of interest?", UID='C00087', answer_type='MultiChoice',
                                      instructions="To ensure transparency and avoid conflicts of interests as much as possible, NITAGs should require all members to declare their interests prior to official appointment. A conflict of interest occurs in the case of the member having a personal investment, activity, or relationship which may affect, or appear to affect, their responsibilities of the NITAG. A conflict of interest, whether real or perceived, can compromise the quality of the recommendations made by the group and can compromise the reputation and integrity of the NITAG. It can also compromise the credibility of the group, even if it would not influence the recommendations. Therefore, interests should be declared prior to the individual's official appointment as a core member. The individual should only be appointed as a member if the person is considered an independent expert so that that their interests do not compromise the integrity of the NITAG.")
QuestionOption.objects.create(text="Yes", question=question_12)
QuestionOption.objects.create(text="No", question=question_12)
QuestionOption.objects.create(text="NR", question=question_12)

question_13 = Question.objects.create(text="Does the advisory group have a website or webpage? If yes, please provide the address in next box (explanatory comments)", UID='C00088', answer_type='MultiChoice',
                                      instructions=" WHO  encourages sharing experiences between countries and their NITAGs. In order to facilitate experience sharing process, WHO would like to circulate website or webpage addresses of NITAGs to others interested.")
QuestionOption.objects.create(text="Yes", question=question_13)
QuestionOption.objects.create(text="No", question=question_13)
QuestionOption.objects.create(text="NR", question=question_13)

parent2 = QuestionGroup.objects.create(subsection=sub_section1, order=1)
parent2.question.add(question_1, question_2, question_3, question_10, question_11, question_12, question_13)
QuestionGroupOrder.objects.create(question=question_1, question_group=parent2, order=1)
QuestionGroupOrder.objects.create(question=question_2, question_group=parent2, order=2)
QuestionGroupOrder.objects.create(question=question_3, question_group=parent2, order=3)

parent3 = QuestionGroup.objects.create(subsection=sub_section1, order=2, parent=parent2,
                                       name="Are the following areas of expertise represented in the group as core membership?",
instructions="It should be noted that it is difficult to fully specify the minimum type of expertise required but it is very important to stress the need for expertise in pediatrics, public health, infectious diseases, epidemiology and immunology. NITAG may have additional expertise and that more expertise is useful.")
parent3.question.add(question_4, question_5, question_6, question_7, question_8, question_9)

QuestionGroupOrder.objects.create(question=question_4, question_group=parent2, order=4)
QuestionGroupOrder.objects.create(question=question_5, question_group=parent2, order=5)
QuestionGroupOrder.objects.create(question=question_6, question_group=parent2, order=6)
QuestionGroupOrder.objects.create(question=question_7, question_group=parent2, order=7)
QuestionGroupOrder.objects.create(question=question_8, question_group=parent2, order=8)
QuestionGroupOrder.objects.create(question=question_9, question_group=parent2, order=9)
QuestionGroupOrder.objects.create(question=question_10, question_group=parent2, order=10)
QuestionGroupOrder.objects.create(question=question_11, question_group=parent2, order=11)
QuestionGroupOrder.objects.create(question=question_12, question_group=parent2, order=12)
QuestionGroupOrder.objects.create(question=question_13, question_group=parent2, order=13)

################################################################################################
sub_section2 = SubSection.objects.create(order=3, section=section_1, title="District coverage reported for routine immunization services in 2013")

question_1 = Question.objects.create(text="DTP3", UID='C00089', answer_type='MultiChoice', is_primary=True)
question_2 = Question.objects.create(text="Coverage is <50%", UID='C00090', answer_type='Number')
question_3 = Question.objects.create(text="Coverage is 50-79%", UID='C00091', answer_type='Number')
question_4 = Question.objects.create(text="Coverage is 80-89%", UID='C00092', answer_type='Number')
question_5 = Question.objects.create(text="Coverage is 90-94%", UID='C00093', answer_type='Number')
question_6 = Question.objects.create(text="Coverage is >=95%", UID='C00094', answer_type='Number')
question_6b = Question.objects.create(text="number of districts not reporting", UID='C0094b', answer_type='Number')

QuestionOption.objects.create(text="Number of districts with DTP3 coverage in each range", question=question_1)
QuestionOption.objects.create(text="Number of surviving infants in these districts", question=question_1)
QuestionOption.objects.create(text="Number of districts reporting DTP drop-out rates greater than 10%", question=question_1)

parent4 = QuestionGroup.objects.create(subsection=sub_section2, order=1, allow_multiples=False, grid=True, display_all=True)
parent4.question.add(question_1, question_2, question_3, question_4, question_5, question_6, question_6b)
QuestionGroupOrder.objects.create(question=question_1, question_group=parent4, order=1)
QuestionGroupOrder.objects.create(question=question_2, question_group=parent4, order=2)
QuestionGroupOrder.objects.create(question=question_3, question_group=parent4, order=3)
QuestionGroupOrder.objects.create(question=question_4, question_group=parent4, order=4)
QuestionGroupOrder.objects.create(question=question_5, question_group=parent4, order=5)
QuestionGroupOrder.objects.create(question=question_6, question_group=parent4, order=6)
QuestionGroupOrder.objects.create(question=question_6b, question_group=parent4, order=7)


question_7 = Question.objects.create(text="Measles", UID='C00095', answer_type='MultiChoice', is_primary=True)
QuestionOption.objects.create(text="Number of districts with measles (MCV1) coverage in each range", question=question_7)
QuestionOption.objects.create(text="Number of surviving infants in these districts", question=question_7)

parent5 = QuestionGroup.objects.create(subsection=sub_section2, order=2, allow_multiples=False, grid=True, display_all=True)
parent5.question.add(question_7, question_2, question_3, question_4, question_5, question_6)
QuestionGroupOrder.objects.create(question=question_7, question_group=parent5, order=1)
QuestionGroupOrder.objects.create(question=question_2, question_group=parent5, order=2)
QuestionGroupOrder.objects.create(question=question_3, question_group=parent5, order=3)
QuestionGroupOrder.objects.create(question=question_4, question_group=parent5, order=4)
QuestionGroupOrder.objects.create(question=question_5, question_group=parent5, order=5)
QuestionGroupOrder.objects.create(question=question_6, question_group=parent5, order=6)
QuestionGroupOrder.objects.create(question=question_6b, question_group=parent5, order=7)

question_8 = Question.objects.create(text="TT2+ (pregnant women)", UID='C00096', answer_type='MultiChoice', is_primary=True)
QuestionOption.objects.create(text="Number of districts with TT2+ coverage in each range", question=question_8)
QuestionOption.objects.create(text="Number of live births in these districts", question=question_8)

parent6 = QuestionGroup.objects.create(subsection=sub_section2, order=3, allow_multiples=False, grid=True, display_all=True)
parent6.question.add(question_8, question_2, question_3, question_4, question_5, question_6)
QuestionGroupOrder.objects.create(question=question_8, question_group=parent6, order=1)
QuestionGroupOrder.objects.create(question=question_2, question_group=parent6, order=2)
QuestionGroupOrder.objects.create(question=question_3, question_group=parent6, order=3)
QuestionGroupOrder.objects.create(question=question_4, question_group=parent6, order=4)
QuestionGroupOrder.objects.create(question=question_5, question_group=parent6, order=5)
QuestionGroupOrder.objects.create(question=question_6, question_group=parent6, order=6)
QuestionGroupOrder.objects.create(question=question_6b, question_group=parent6, order=7)

question_9 = Question.objects.create(text="PAB (protection at birth)", UID='C00097', answer_type='MultiChoice', is_primary=True)
QuestionOption.objects.create(text="Number of districts with PAB coverage in each range", question=question_9)
QuestionOption.objects.create(text="Number of live births in these districts", question=question_9)

parent7 = QuestionGroup.objects.create(subsection=sub_section2, order=4, allow_multiples=False, grid=True, display_all=True)
parent7.question.add(question_9, question_2, question_3, question_4, question_5, question_6)
QuestionGroupOrder.objects.create(question=question_9, question_group=parent7, order=1)
QuestionGroupOrder.objects.create(question=question_2, question_group=parent7, order=2)
QuestionGroupOrder.objects.create(question=question_3, question_group=parent7, order=3)
QuestionGroupOrder.objects.create(question=question_4, question_group=parent7, order=4)
QuestionGroupOrder.objects.create(question=question_5, question_group=parent7, order=5)
QuestionGroupOrder.objects.create(question=question_6, question_group=parent7, order=6)
QuestionGroupOrder.objects.create(question=question_6b, question_group=parent7, order=7)

################################################################################################
sub_section3 = SubSection.objects.create(order=4, section=section_1)

question_1 = Question.objects.create(text="Number of districts reporting DTP drop-out rates greater than 10%", UID='C00098', answer_type='Number', instructions="Drop-out rate = (DTP1-DTP3) x 100 / DTP1")

parent8 = QuestionGroup.objects.create(subsection=sub_section3, order=1)
parent8.question.add(question_1)
QuestionGroupOrder.objects.create(question=question_1, question_group=parent8, order=1)

################################################################################################
sub_section4 = SubSection.objects.create(order=5, section=section_1, title="Vaccine supply for routine services")

question_1 = Question.objects.create(text="Vaccine/Supplies", UID='C00099', answer_type='MultiChoice', instructions="Please complete separately for each vaccine, even if they were given in combination")
QuestionOption.objects.create(text="BCG", question=question_1)
QuestionOption.objects.create(text="DTP vaccines", question=question_1)
QuestionOption.objects.create(text="Hepatitis B-containing vaccines", question=question_1)
QuestionOption.objects.create(text="Hib-containing vaccines", question=question_1)
QuestionOption.objects.create(text="Pneumococcal conjugate vaccine", question=question_1)
QuestionOption.objects.create(text="Rotavirus", question=question_1)
QuestionOption.objects.create(text="Polio (OPV or IPV)", question=question_1)
QuestionOption.objects.create(text="Measles-containing vaccines", question=question_1)
QuestionOption.objects.create(text="Yellow fever", question=question_1)
QuestionOption.objects.create(text="Tetanus toxoid", question=question_1)

parent9 = QuestionGroup.objects.create(subsection=sub_section4, order=1, allow_multiples=True)
parent9.question.add(question_1)

##################
#start of subgroup
question_2 = Question.objects.create(text="Was there a stock-out (no remaining doses for any period of time) at the national level during 2013?", UID='C00100', answer_type='MultiChoice', instructions="If a vaccine is not currently in use, select \"NR\" (not relevant) from the drop-down menu.")
QuestionOption.objects.create(text="Yes", question=question_2)
QuestionOption.objects.create(text="No", question=question_2)
QuestionOption.objects.create(text="NR", question=question_2)

question_3 = Question.objects.create(text="public health", UID='C00101', answer_type='Number', instructions="If the stock-out lasted less than one month (for example, a few days or weeks), enter \"1\".")

parent10 = QuestionGroup.objects.create(subsection=sub_section4, order=2, parent=parent9, name="National store")
parent10.question.add(question_2, question_3)
#end of subgroup
##################

##################
#start of subgroup
question_4 = Question.objects.create(text="Was there a stock-out in any district during 2013?", UID='C00102', answer_type='MultiChoice',
                                     instructions="Districts can experience stock-outs even if there was no stock-out at the national level. Therefore, the answer in column C may be \"yes\" even if the answer in column A is \"no\".\nIf a vaccine is not currently in use, select \"NR\" (not relevant) from the drop-down menu in column C.\n\nIf a district has no permanent vaccine store (i.e., the store is located at the provincial or higher level) but health units have been affected by vaccine shortages, select \"yes\" from the drop-down menu in column C and count the district in column D.")
QuestionOption.objects.create(text="Yes", question=question_4)
QuestionOption.objects.create(text="No", question=question_4)
QuestionOption.objects.create(text="NR", question=question_4)

question_5 = Question.objects.create(text="If yes, indicate the number of districts with interruption of activities due to stock-outs", UID='C00103', answer_type='Number',
                                     instructions="Districts can experience stock-outs even if there was no stock-out at the national level. Therefore, the answer in column C may be \"yes\" even if the answer in column A is \"no\".\nIf a vaccine is not currently in use, select \"NR\" (not relevant) from the drop-down menu in column C.\n\nIf a district has no permanent vaccine store (i.e., the store is located at the provincial or higher level) but health units have been affected by vaccine shortages, select \"yes\" from the drop-down menu in column C and count the district in column D.")

parent11 = QuestionGroup.objects.create(subsection=sub_section4, order=3, parent=parent9, name="District stores")
parent11.question.add(question_4, question_5)
#end of subgroup
##################

##################
#start of subgroup

question_6 = Question.objects.create(text="Wastage (%) Please complete separately for each vaccine, even if they were given in combination", UID='C00104', answer_type='Number',
                                     instructions="List the percentage of vaccine wasted throughout the country in opened vials at the service delivery points. Enter \"ND\" if no data are available. Please enter a value for the wastage rate for each vaccine listed, even if the vaccines were given in combination.")

parent12 = QuestionGroup.objects.create(subsection=sub_section4, order=4, parent=parent9, name="Wastage")
parent12.question.add(question_6)
#end of subgroup
##################

QuestionGroupOrder.objects.create(question=question_1, question_group=parent9, order=1)
QuestionGroupOrder.objects.create(question=question_2, question_group=parent9, order=2)
QuestionGroupOrder.objects.create(question=question_3, question_group=parent9, order=3)
QuestionGroupOrder.objects.create(question=question_4, question_group=parent9, order=4)
QuestionGroupOrder.objects.create(question=question_5, question_group=parent9, order=5)
QuestionGroupOrder.objects.create(question=question_6, question_group=parent9, order=6)

################################################################################################
sub_section5 = SubSection.objects.create(order=6, section=section_1, title="Safety Data")

question_1 = Question.objects.create(text="In 2013 was a policy being implemented for immunization injection safety?", UID='C00105', answer_type='MultiChoice')
QuestionOption.objects.create(text="Yes", question=question_1)
QuestionOption.objects.create(text="No", question=question_1)
QuestionOption.objects.create(text="NR", question=question_1)
QuestionOption.objects.create(text="ND", question=question_1)

question_2 = Question.objects.create(text="Does your country have a vaccine adverse events review committee? ", UID='C00106', answer_type='MultiChoice',
                                     instructions="Adverse events review committee is an independent committee of recognized experts that provides technical advice and recommendations to the government regarding vaccine safety issues. The adverse events review committee is a tool that enables the government to assess vaccine safety issues through a transparent, systematic process. The adverse events review committees are composed of recognized national experts, independent from the immunization program and the national regulatory authority, and their primary function should focus on offering technical recommendations. Please note that countries that have an ad hoc committee should mark the \"No\" option, as the question is asking for existence of a standing committee.")
QuestionOption.objects.create(text="Yes", question=question_2)
QuestionOption.objects.create(text="No", question=question_2)
QuestionOption.objects.create(text="NR", question=question_2)
QuestionOption.objects.create(text="ND", question=question_2)

question_3 = Question.objects.create(text="Is there a national system to monitor adverse events following immunization?", UID='C00107', answer_type='MultiChoice',
                                     instructions="A national system must include ALL of the following:<br/>1) written guidelines on monitoring and investigation of reported adverse events;<br/>2) a written list of events to monitor;<br/>3) an established mechanism to communicate data for regulatory action; and<br/>4) implementation of points 1, 2 and 3.<br/><br/>If any of the four conditions are not met, select \"no\".")
QuestionOption.objects.create(text="Yes", question=question_3)
QuestionOption.objects.create(text="No", question=question_3)
QuestionOption.objects.create(text="NR", question=question_3)
QuestionOption.objects.create(text="ND", question=question_3)

question_4 = Question.objects.create(text="If yes, how many total  adverse events, including suspected or confirmed, were reported to the national level in 2013?", UID='C00108', answer_type='Number')

question_5 = Question.objects.create(text="In 2013 was there  a national policy for waste from immunization activities?", UID='C00127', answer_type='MultiChoice')
QuestionOption.objects.create(text="Yes", question=question_5)
QuestionOption.objects.create(text="No", question=question_5)
QuestionOption.objects.create(text="NR", question=question_5)
QuestionOption.objects.create(text="ND", question=question_5)

parent13 = QuestionGroup.objects.create(subsection=sub_section5, order=1)
parent13.question.add(question_1, question_2, question_3, question_4, question_5)

##################
#start of subgroup
question_6 = Question.objects.create(text="Incineration", UID='C00109', answer_type='MultiChoice')
QuestionOption.objects.create(text="Yes", question=question_6)
QuestionOption.objects.create(text="No", question=question_6)

question_7 = Question.objects.create(text="Open burning", UID='C00110', answer_type='MultiChoice')
QuestionOption.objects.create(text="Yes", question=question_7)
QuestionOption.objects.create(text="No", question=question_7)

question_8 = Question.objects.create(text="Burial", UID='C00111', answer_type='MultiChoice')
QuestionOption.objects.create(text="Yes", question=question_8)
QuestionOption.objects.create(text="No", question=question_8)

question_9 = Question.objects.create(text="Other", UID='C00112', answer_type='MultiChoice')
QuestionOption.objects.create(text="Yes", question=question_9)
QuestionOption.objects.create(text="No", question=question_9)

parent14 = QuestionGroup.objects.create(subsection=sub_section5, order=2, parent=parent13,
                                        name="What was the recommended practice for disposal of immunization waste in 2013? Pick \"yes\" for all that apply.",
                                        instructions="<strong>Incineration</strong> refers to closed methods of burning at temperatures greater or equal to 800\&deg;C.<br/><strong>Open burning</strong> refers to pit burning and drum burning.<br/><strong>Burial</strong> refers to waste burial pits and encapsulation with cement or another immobilizing agent, such as sand or plaster.<br/><strong>Other</strong> refers to any waste-disposal policy or practice that is not listed above. If you answer \"yes\" to this item, please describe these other policies and practices in the answer to the next question.")
parent14.question.add(question_6, question_7, question_8, question_9)
#end of subgroup
##################

QuestionGroupOrder.objects.create(question=question_1, question_group=parent13, order=1)
QuestionGroupOrder.objects.create(question=question_2, question_group=parent13, order=2)
QuestionGroupOrder.objects.create(question=question_3, question_group=parent13, order=3)
QuestionGroupOrder.objects.create(question=question_4, question_group=parent13, order=4)
QuestionGroupOrder.objects.create(question=question_5, question_group=parent13, order=5)
QuestionGroupOrder.objects.create(question=question_6, question_group=parent13, order=6)
QuestionGroupOrder.objects.create(question=question_7, question_group=parent13, order=7)
QuestionGroupOrder.objects.create(question=question_8, question_group=parent13, order=8)
QuestionGroupOrder.objects.create(question=question_9, question_group=parent13, order=9)
################################################################################################

sub_section6 = SubSection.objects.create(order=7, section=section_1, title="Financing Data")
parent15 = QuestionGroup.objects.create(subsection=sub_section6, order=1)

##################
#start of subgroup
question_1 = Question.objects.create(text="the purchase of vaccines used in routine immunizations", UID='C00113', answer_type='MultiChoice')
QuestionOption.objects.create(text="Yes", question=question_1)
QuestionOption.objects.create(text="No", question=question_1)
QuestionOption.objects.create(text="NR", question=question_1)
QuestionOption.objects.create(text="ND", question=question_1)

question_2 = Question.objects.create(text="the purchase of injection supplies (such as syringes, needles, and safety boxes) for routine immunizations", UID='C00114', answer_type='MultiChoice')
QuestionOption.objects.create(text="Yes", question=question_2)
QuestionOption.objects.create(text="No", question=question_2)
QuestionOption.objects.create(text="NR", question=question_2)
QuestionOption.objects.create(text="ND", question=question_2)

question_3 = Question.objects.create(text="the health care waste management ", UID='C00128', answer_type='MultiChoice')
QuestionOption.objects.create(text="Yes", question=question_3)
QuestionOption.objects.create(text="No", question=question_3)
QuestionOption.objects.create(text="NR", question=question_3)
QuestionOption.objects.create(text="ND", question=question_3)

parent16 = QuestionGroup.objects.create(subsection=sub_section6, order=2, parent=parent15,
                                        name="Are there line items in the national government budget specifically  for: ",
                                        instructions="Countries that have specific line items in the national budget for i) the purchase of vaccines used in routine immunizations, ii) the purchase of injection supplies and iii) the health care waste management should report yes respectively to these questions. Countries that do not have specific budget lines or have a general budget for health that includes vaccines, supplies and waste management should report no respectively to these questions.")
parent16.question.add(question_1, question_2, question_3)
#end of subgroup
##################

##################
#start of subgroup
question_4 = Question.objects.create(text="Amount", UID='C00115', answer_type='Number')

question_5 = Question.objects.create(text="Currency", UID='C00116', answer_type='MultiChoice')
QuestionOption.objects.create(text="local currency", question=question_5)
QuestionOption.objects.create(text="US $", question=question_5)

parent17 = QuestionGroup.objects.create(subsection=sub_section6, order=2, parent=parent15,
                                        name="What amount of government funds was spent on vaccines used in routine immunization?",
                                        instructions="This figure should be available from multi-year plan for immunization with a costing and financing component. Government includes all administrative levels such as national and sub-national governments, all funds allocated through the National Government Budget. Extra-budgetary financing from donors, out-of-pocket and informal private payments are excluded.")
parent17.question.add(question_4, question_5)
#end of subgroup
##################

##################
#start of subgroup
question_6 = Question.objects.create(text="Amount", UID='C00117', answer_type='Number')

question_7 = Question.objects.create(text="Currency", UID='C00118', answer_type='MultiChoice')
QuestionOption.objects.create(text="local currency", question=question_7)
QuestionOption.objects.create(text="US $", question=question_7)

parent18 = QuestionGroup.objects.create(subsection=sub_section6, order=3, parent=parent15,
                                        name="What is the total expenditure (from all sources) on vaccines used in routine immunization?",
                                        instructions="This figure should be available from multi-year plan for immunization with a costing and financing component. It includes all sources of financing vaccines used in routine immunization (e.g. government, health insurance, donors, out-of-pocket and informal private payments)")
parent18.question.add(question_6, question_7)
#end of subgroup
##################

question_8 = Question.objects.create(text="If total amounts are not available for the previous questions please provide an estimated percentage of  total expenditure on vaccines financed by government funds", UID='C00119', answer_type='Number',
                                     instructions="Give the percentage of  expenditure on vaccines used in routine immunization that was financed solely with government funds. Government includes all administrative levels such as national and sub-national governments. The estimate can come from a previous year or a \"best guess\"")

##################
#start of subgroup
question_9 = Question.objects.create(text="Amount", UID='C00120', answer_type='Number')

question_10 = Question.objects.create(text="Currency", UID='C00121', answer_type='MultiChoice')
QuestionOption.objects.create(text="local currency", question=question_10)
QuestionOption.objects.create(text="US $", question=question_10)

parent19 = QuestionGroup.objects.create(subsection=sub_section6, order=4, parent=parent15,
                                        name="What amount of government funds was spent on routine immunization?",
                                        instructions="This figure should be available from multi-year plan for immunization with a costing and financing component. It includes all recurrent, immunization-specific expenditure of routine immunization. In particular, recurrent inputs include vaccines, injection supplies, salaries and per diems of health staff working full-time on immunization, transport, vehicles and cold chain maintenance, training, social mobilization, and monitoring and surveillance.  Government includes all administrative levels such as national and sub-national governments, all fund allocated through the National Government Budget. Extra-budgetary financing from donors, out-of-pocket and informal private payments are excluded.")
parent19.question.add(question_9, question_10)
#end of subgroup
##################

##################
#start of subgroup
question_11 = Question.objects.create(text="Amount", UID='C00122', answer_type='Number')

question_12 = Question.objects.create(text="Currency", UID='C00123', answer_type='MultiChoice')
QuestionOption.objects.create(text="local currency", question=question_12)
QuestionOption.objects.create(text="US $", question=question_12)

parent20 = QuestionGroup.objects.create(subsection=sub_section6, order=4, parent=parent15,
                                        name="What is the total expenditure (from all sources) on routine immunization?",
                                        instructions="This figure should be available from multi-year plan for immunization with a costing and financing component. It includes all recurrent, immunization-specific expenditure of routine immunization. In particular, recurrent inputs include vaccines, injection supplies, salaries and per diems of health staff working full-time on immunization, transport, vehicles and cold chain maintenance, training, social mobilization, and monitoring and surveillance. It includes all sources of financing routine immunization (e.g. government, health insurance, donors, out-of-pocket and informal private payments).")
parent20.question.add(question_11, question_12)
#end of subgroup
##################

question_13 = Question.objects.create(text="If total amounts are not available for the previous question please provide an estimated percentage of total expenditure on routine immunization  financed by government funds?", UID='C00124', answer_type='Number',
                                     instructions="Give the percentage of expenditure on routine immunization that was financed solely with government funds. Government includes all administrative levels such as national and sub-national governments. The estimate can come from a previous year or a \"best guess\".")

parent15.question.add(question_8, question_13)

QuestionGroupOrder.objects.create(question=question_1, question_group=parent15, order=1)
QuestionGroupOrder.objects.create(question=question_2, question_group=parent15, order=2)
QuestionGroupOrder.objects.create(question=question_3, question_group=parent15, order=3)
QuestionGroupOrder.objects.create(question=question_4, question_group=parent15, order=4)
QuestionGroupOrder.objects.create(question=question_5, question_group=parent15, order=5)
QuestionGroupOrder.objects.create(question=question_6, question_group=parent15, order=6)
QuestionGroupOrder.objects.create(question=question_7, question_group=parent15, order=7)
QuestionGroupOrder.objects.create(question=question_8, question_group=parent15, order=8)
QuestionGroupOrder.objects.create(question=question_9, question_group=parent15, order=9)
QuestionGroupOrder.objects.create(question=question_10, question_group=parent15, order=10)
QuestionGroupOrder.objects.create(question=question_11, question_group=parent15, order=11)
QuestionGroupOrder.objects.create(question=question_12, question_group=parent15, order=12)
QuestionGroupOrder.objects.create(question=question_13, question_group=parent15, order=13)

# data = serializers.serialize("json", [section_1, sub_section, sub_section1, sub_section2, sub_section3, sub_section4,
#                                       sub_section5, sub_section6])
# print data
#
# data = serializers.serialize("json", [parent1, parent2, parent3, parent4, parent5, parent6, parent7, parent8, parent9,
#                                       parent10, parent11, parent12, parent13, parent14, parent15, parent16, parent17,
#                                       parent18, parent19, parent20])
# print data
#
# data = serializers.serialize("json", parent1.question.all())
# print data
#
# data = serializers.serialize("json", parent2.question.all())
# print data
#
# data = serializers.serialize("json", parent3.question.all())
# print data
#
# data = serializers.serialize("json", parent4.question.all())
# print data
#
# data = serializers.serialize("json", parent5.question.all())
# print data
#
# data = serializers.serialize("json", parent6.question.all())
# print data
#
# data = serializers.serialize("json", parent7.question.all())
# print data
#
# data = serializers.serialize("json", parent8.question.all())
# print data
#
# data = serializers.serialize("json", parent9.question.all())
# print data
#
# data = serializers.serialize("json", parent10.question.all())
# print data
#
# data = serializers.serialize("json", parent11.question.all())
# print data
#
# data = serializers.serialize("json", parent12.question.all())
# print data
#
#
# data = serializers.serialize("json", parent13.question.all())
# print data
#
#
# data = serializers.serialize("json", parent14.question.all())
# print data
#
#
# data = serializers.serialize("json", parent15.question.all())
# print data
#
#
# data = serializers.serialize("json", parent16.question.all())
# print data
#
#
# data = serializers.serialize("json", parent17.question.all())
# print data
#
#
# data = serializers.serialize("json", parent18.question.all())
# print data
#
#
# data = serializers.serialize("json", parent19.question.all())
# print data
#
#
# data = serializers.serialize("json", parent20.question.all())
# print data
#
# data = serializers.serialize("json", parent1.orders.all())
# print data
#
# data = serializers.serialize("json", parent2.orders.all())
# print data
#
# data = serializers.serialize("json", parent3.orders.all())
# print data
#
# data = serializers.serialize("json", parent4.orders.all())
# print data
#
# data = serializers.serialize("json", parent5.orders.all())
# print data
#
# data = serializers.serialize("json", parent6.orders.all())
# print data
#
# data = serializers.serialize("json", parent7.orders.all())
# print data
#
# data = serializers.serialize("json", parent8.orders.all())
# print data
#
# data = serializers.serialize("json", parent9.orders.all())
# print data
#
# data = serializers.serialize("json", parent10.orders.all())
# print data
#
# data = serializers.serialize("json", parent11.orders.all())
# print data
#
# data = serializers.serialize("json", parent12.orders.all())
# print data
#
# data = serializers.serialize("json", parent13.orders.all())
# print data
#
# data = serializers.serialize("json", parent14.orders.all())
# print data
#
# data = serializers.serialize("json", parent15.orders.all())
# print data
#
# data = serializers.serialize("json", parent16.orders.all())
# print data
#
# data = serializers.serialize("json", parent17.orders.all())
# print data
#
# data = serializers.serialize("json", parent18.orders.all())
# print data
#
# data = serializers.serialize("json", parent19.orders.all())
# print data
#
# data = serializers.serialize("json", parent20.orders.all())
# print data
