from questionnaire.models import Questionnaire, Section, SubSection, Question, QuestionGroup, QuestionOption, QuestionGroupOrder
from django.core import serializers

questionnaire = Questionnaire.objects.get(name="JRF 2013 Core English", description="From dropbox as given by Rouslan")

section_1 = Section.objects.create(order=2, title="Immunization Schedule for 2013", description="""
Describe the 2013 national immunization schedule for routine services in the following table. Include all doses administered to young children, adolescents, and adults on a routine basis. Each row describes a vaccine or combination vaccine. Include vitamin A if it is delivered through routine immunization services. Also include information about the use of auto-disable (AD) syringes. <br/>
If there are plans to introduce a vaccine, supplement, or syringe, enter the month and year that the introduction is planned in column G.<br/>
If the immunization schedule includes other vaccines that are not listed, add them at the bottom of the table.<br/>""",
                        questionnaire=questionnaire, name="Schedule-Source")
sub_section = SubSection.objects.create(order=1, section=section_1,
description="Use this section to describe the 2013 national immunization schedule and any planned vaccine introductions. Complete the rows for all vaccines and supplements currently in use in the country. ")

question1 = Question.objects.create(text="Vaccine, Supplement, or Injection Equipment",
                                    UID='C00031', answer_type='MultiChoice', is_primary=True)
question1b = Question.objects.create(text="Type",
                                    UID='C0031b', answer_type='MultiChoice',)

question2 = Question.objects.create(text="1st dose", UID='C00032', answer_type='Text', export_label='1st dose')
question3 = Question.objects.create(text="2nd dose", UID='C00033', answer_type='Text', export_label='2nd dose')
question4 = Question.objects.create(text="3rd dose", UID='C00034', answer_type='Text', export_label='3rd dose')
question5 = Question.objects.create(text="4th dose", UID='C00035', answer_type='Text', export_label='4th dose')
question6 = Question.objects.create(text="5th dose", UID='C00036', answer_type='Text', export_label='5th dose')
question7 = Question.objects.create(text="6th dose", UID='C00037', answer_type='Text', export_label='6th dose')

question8 = Question.objects.create(text="Planned introduction", UID='C00038', answer_type='Date', export_label='Planned introduction')

question10 = Question.objects.create(text="Geo-graphic area", UID='C00040', answer_type='MultiChoice',
                                     export_label='Geographic Area',
instructions='If a vaccine or supplement is given throughout the entire country, pick "national" from the drop-down list. If it is given only in certain regions of the country, pick "subnational". This column refers only to geographical areas and not to special target or risk groups.')

question11 = Question.objects.create(text="Specific target group", UID='C00041', answer_type='Text',
                                     export_label=' Specific target groups',
instructions='If a vaccine is not given to the entire population, specify the target group (for example, adults over 65, travellers, diabetes patients, or displaced persons).')

question12 = Question.objects.create(text="Name of manufacturer", export_label='Manufacturer', UID='C00042', answer_type='Text',
instructions='Indicate the origin for all vaccines and supplements used in the country and also for auto-disable (AD) syringes. If AD syringes are not used in the country, leave those cells blank.')

question13 = Question.objects.create(text="Which agency procured the vaccine?", export_label='Procurement source',UID='C00043', answer_type='MultiChoice',
instructions="""
There are four possible answers:
<ul>
<li> the vaccine was procured by the supply division of the MOH or some other governmental agency</li>
<li> the vaccine was procured through UNICEF, WHO, or PAHO</li>
<li> the vaccine was procured through a donating agency, business, or person </li>
<li> the vaccine was procured through some other organization or source not listed above</li>
</ul>
""")

question14 = Question.objects.create(text="Total no. of doses procured at national level",
                                     export_label='Total no. procured at national level', UID='C00044', answer_type='Number',
instructions= 'Indicate how many doses of each type of vaccine and supplement were procured at the national level.')

QuestionOption.objects.create(text="BCG: Bacille Calmette-Guerin vaccine", question=question1)
QuestionOption.objects.create(text="DTP: Diphtheria and tetanus toxoid with pertussis vaccine", question=question1)
QuestionOption.objects.create(text="DTPHepB: Diphtheria and tetanus toxoid with pertussis and HepB vaccine", question=question1)
QuestionOption.objects.create(text='"DTPHepB IPV": Diphtheria and tetanus toxoid with pertussis, HepB and IPV vaccine', question=question1)
QuestionOption.objects.create(text='"DTPHib HepB": Diphtheria and tetanus toxoid with pertussis, Hib and HepB vaccine', question=question1)
QuestionOption.objects.create(text="DTPHib: Diphtheria and tetanus toxoid with pertussis and Hib vaccine", question=question1)
QuestionOption.objects.create(text="DTPHib IPV: Diphtheria and tetanus toxoid with pertussis, Hib and IPV vaccine", question=question1)
QuestionOption.objects.create(text="DTPHib HepBIPV: Diphtheria and tetanus toxoid with pertussis, Hib, hepatitis B and IPV vaccine", question=question1)
QuestionOption.objects.create(text="DTPIPV: Diphtheria and tetanus toxoid with pertussis vaccine and IPV", question=question1)
QuestionOption.objects.create(text="Dip: Diphtheria vaccine", question=question1)
QuestionOption.objects.create(text="DT: Tetanus and diphtheria toxoid, children's dose", question=question1)
QuestionOption.objects.create(text="Td: Tetanus and diphtheria toxoid for older children and adults", question=question1)
QuestionOption.objects.create(text="TdaP: Tetanus, diphtheria toxoid, acelular perussis for older children and adults", question=question1)
QuestionOption.objects.create(text="TT: Tetanus toxoid", question=question1)
QuestionOption.objects.create(text="P: Pertussis vaccine", question=question1)
QuestionOption.objects.create(text="HepA: Hepatitis A vaccine", question=question1)
QuestionOption.objects.create(text="HepB_Adult: Adult Hepatitis B vaccine", question=question1)
QuestionOption.objects.create(text="HepB_Pediatric: Pediatric Hepatitis B vaccine", question=question1)
QuestionOption.objects.create(text="Hib: Haemophilus influenza type b vaccine", question=question1)
QuestionOption.objects.create(text="OPV: Oral polio vaccine", question=question1)
QuestionOption.objects.create(text="IPV: Inactivated polio vaccine", question=question1)
QuestionOption.objects.create(text="Measles: Measles vaccine", question=question1)
QuestionOption.objects.create(text="MM: Measles and mumps vaccine", question=question1)
QuestionOption.objects.create(text="MR: Measles and rubella vaccine", question=question1)
QuestionOption.objects.create(text="MMR: Measles, mumps and rubella vaccine", question=question1)
QuestionOption.objects.create(text="Mumps: Mumps vaccine", question=question1)
QuestionOption.objects.create(text="JE_LiveAtd: Japanese encephalitis live attenuated vaccine", question=question1)
QuestionOption.objects.create(text="JE_Inactd: Japanese encephalitis inactivated vaccine", question=question1)
QuestionOption.objects.create(text="Influenza_Adult: Adult seasonal influenza vaccine", question=question1)
QuestionOption.objects.create(text="Influenza_Pediatric: Pediatrict seasonal influenza vaccine", question=question1)
QuestionOption.objects.create(text="MenC_conj: Meningococcal C conjugate vaccine", question=question1)
QuestionOption.objects.create(text="Men AC: Meningococcal AC ", question=question1)
QuestionOption.objects.create(text="Men ACW: Meningococcal ACW", question=question1)
QuestionOption.objects.create(text="Men ACWY: Meningococcal ACWY", question=question1)
QuestionOption.objects.create(text="Men A: Meningococcal A conjugate vaccine", question=question1)
QuestionOption.objects.create(text="Pneumoco_ conj: Pneumococcal conjugate vaccine: No. of valents", question=question1)
QuestionOption.objects.create(text="Pneumo_ps: Pneumococcal polysaccharide vaccine", question=question1)
QuestionOption.objects.create(text="Rubella: Rubella vaccine", question=question1)
QuestionOption.objects.create(text="Typhoid: Typhoid fever vaccine", question=question1)
QuestionOption.objects.create(text="Varicella: Varicella vaccine", question=question1)
QuestionOption.objects.create(text="YF: Yellow fever vaccine", question=question1)
QuestionOption.objects.create(text="Rotavirus: Rotavirus vaccine: No. of valents", question=question1)
QuestionOption.objects.create(text="HPV: Human papillomavirus  vaccine: No. of valents", question=question1)
QuestionOption.objects.create(text="Vit A: Vitamin A supplements", question=question1)

QuestionOption.objects.create(text="Acellular", question=question1b)
QuestionOption.objects.create(text="Whole cell", question=question1b)

QuestionOption.objects.create(text="Subnational", question=question10)
QuestionOption.objects.create(text="National", question=question10)

QuestionOption.objects.create(text="government agency", question=question13)
QuestionOption.objects.create(text="UNICEF, WHO or PAHO", question=question13)
QuestionOption.objects.create(text="donating agency", question=question13)
QuestionOption.objects.create(text="other", question=question13)


parent = QuestionGroup.objects.create(subsection=sub_section, order=1, grid=True, allow_multiples=True, hybrid=True)
parent.question.add(question1, question1b, question8, question10, question11)

subgroup = QuestionGroup.objects.create(subsection=sub_section, parent=parent, name="Recommended age of admnistration", grid=True)
subgroup.question.add(question2, question3, question4, question5, question6, question7)


subgroup1 = QuestionGroup.objects.create(subsection=sub_section, parent=parent, name="Source of Vaccines, Vitamin A, and AD Syringes",
                                                     instructions="<p>Record sources of all AD syringes distributed by the Ministry of Health for routine immunizations during the " +
                                                      "reporting period January 1 - December 31, 2013 </p> <p>If manufacturers or procuring agency were used for the same vaccine, list them all. Use the extra rows at the bottom to accomodate this information.</p>"
                                                      )
subgroup1.question.add(question12, question13, question14)

QuestionGroupOrder.objects.create(question=question1, question_group=parent, order=1)
QuestionGroupOrder.objects.create(question=question1b, question_group=parent, order=2)
QuestionGroupOrder.objects.create(question=question2, question_group=parent, order=3)
QuestionGroupOrder.objects.create(question=question3, question_group=parent, order=4)
QuestionGroupOrder.objects.create(question=question4, question_group=parent, order=5)
QuestionGroupOrder.objects.create(question=question5, question_group=parent, order=6)
QuestionGroupOrder.objects.create(question=question6, question_group=parent, order=7)
QuestionGroupOrder.objects.create(question=question7, question_group=parent, order=8)
QuestionGroupOrder.objects.create(question=question8, question_group=parent, order=9)
QuestionGroupOrder.objects.create(question=question10, question_group=parent, order=10)
QuestionGroupOrder.objects.create(question=question11, question_group=parent, order=11)
QuestionGroupOrder.objects.create(question=question12, question_group=parent, order=12)
QuestionGroupOrder.objects.create(question=question13, question_group=parent, order=13)
QuestionGroupOrder.objects.create(question=question14, question_group=parent, order=14)

######################################### next group

question15 = Question.objects.create(text="AD equipment", UID='C00045', answer_type='MultiChoice', is_primary=True)

QuestionOption.objects.create(text="AD - BCG: AD (auto-disable) syringes for BCG", question=question15)
QuestionOption.objects.create(text="AD - inj: AD syringes", question=question15)
QuestionOption.objects.create(text="AD - Rec: AD syringes for reconstitution", question=question15)

question16 = Question.objects.create(text="Which agency procured the Syringes?", export_label='Procurement source',UID='C00046', answer_type='MultiChoice',)

question17 = Question.objects.create(text="Total no. of syringes procured at national level", UID='C00047', export_label='Total no. procured at national level', answer_type='Number',)

parent2 = QuestionGroup.objects.create(subsection=sub_section, order=2, allow_multiples=True, grid=True, hybrid=True)
parent2.question.add(question15, question8, question10, question11)

subgroup2 = QuestionGroup.objects.create(subsection=sub_section, parent=parent2, name="Source of Vaccines, Vitamin A, and AD Syringes",
                                         instructions="<p>Record sources of all AD syringes distributed by the Ministry of Health for routine immunizations during the " +
                                                      "reporting period January 1 - December 31, 2013 </p> <p>If manufacturers or procuring agency were used for the same vaccine, list them all. Use the extra rows at the bottom to accomodate this information.</p>"
                                                      )
subgroup2.question.add(question12, question16, question17)

QuestionOption.objects.create(text="government agency", question=question16)
QuestionOption.objects.create(text="UNICEF, WHO or PAHO", question=question16)
QuestionOption.objects.create(text="donating agency", question=question16)
QuestionOption.objects.create(text="other", question=question16)


QuestionGroupOrder.objects.create(question=question15, question_group=parent2, order=1)
QuestionGroupOrder.objects.create(question=question8, question_group=parent2, order=2)
QuestionGroupOrder.objects.create(question=question10, question_group=parent2, order=3)
QuestionGroupOrder.objects.create(question=question11, question_group=parent2, order=4)
QuestionGroupOrder.objects.create(question=question12, question_group=parent2, order=6)
QuestionGroupOrder.objects.create(question=question16, question_group=parent2, order=7)
QuestionGroupOrder.objects.create(question=question17, question_group=parent2, order=8)

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
