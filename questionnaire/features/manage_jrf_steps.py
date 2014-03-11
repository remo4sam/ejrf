from lettuce import world, step
from splinter import Browser
from questionnaire.features.pages.home import HomePage
from questionnaire.features.pages.users import LoginPage
from questionnaire.models import Questionnaire, Section, Organization, Region


@step(u'I have four finalised questionnaires')
def given_i_have_four_finalised_questionnaires(step):
    world.questionnaire1 = Questionnaire.objects.create(name="JRF Jamaica version", description="description",
                                                        year=2012, status=Questionnaire.FINALIZED)

    Section.objects.create(title="School Based Section1", order=0, questionnaire=world.questionnaire1, name="Name")

    world.questionnaire2 = Questionnaire.objects.create(name="JRF Brazil version", description="description",
                                                        year=2009, status=Questionnaire.FINALIZED)
    Section.objects.create(title="School Section1", order=0, questionnaire=world.questionnaire2, name="Section1 name")
    world.questionnaire3 = Questionnaire.objects.create(name="JRF Bolivia version", description="some more description",
                                                        year=2011, status=Questionnaire.FINALIZED)
    Section.objects.create(title="Section1", order=0, questionnaire=world.questionnaire3, name="School Imm. Delivery")
    world.questionnaire4 = Questionnaire.objects.create(name="JRF kampala version", description="description",
                                                        year=2010, status=Questionnaire.FINALIZED)
    Section.objects.create(title="Section1", order=0, questionnaire=world.questionnaire4, name="School Imm. Delivery")


@step(u'And I have two draft questionnaires for two years')
def and_i_have_two_draft_questionnaires_for_two_years(step):
    world.questionnaire5 = Questionnaire.objects.create(name="JRF Bolivia version", description="some more description",
                                                        year=2013, status=Questionnaire.DRAFT)
    Section.objects.create(title="Section1", order=0, questionnaire=world.questionnaire5, name="School Imm. Delivery")
    world.questionnaire6 = Questionnaire.objects.create(name="JRF kampala version", description="description",
                                                        year=2013, status=Questionnaire.DRAFT)
    Section.objects.create(title="Section1", order=0, questionnaire=world.questionnaire6, name="School Imm. Delivery")


@step(u'Then I should see manage JRF, users, question bank, extract and attachments links')
def then_i_should_see_manage_jrf_users_question_bank_extract_and_attachments_links(step):
    world.page.is_text_present("HOME", "EXTRACT", "ATTACHMENTS", "MANAGE JRF", "USERS", "QUESTION BANK")

@step(u'Then I should see a list of the three most recent finalised questionnaires')
def then_i_should_see_a_list_of_the_three_most_recent_finalised_questionnaires(step):
    world.page = HomePage(world.browser)
    world.page.links_present_by_text(["%s %s" % (world.questionnaire1.name, world.questionnaire1.year),
                                     "%s %s" % (world.questionnaire2.name, world.questionnaire2.year),
                                     "%s %s" % (world.questionnaire3.name, world.questionnaire3.year)])

@step(u'And I should see a list of draft questionnaires')
def and_i_should_see_a_list_of_draft_questionnaires(step):
     world.page.links_present_by_text(["%s %s" % (world.questionnaire5.name, world.questionnaire5.year),
                                     "%s %s" % (world.questionnaire6.name, world.questionnaire6.year)])
     world.page.is_element_present_by_id('id-edit')
     world.page.is_element_present_by_id('id-finalize')

@step(u'I visit the manage JRF page')
def and_i_visit_manage_jrf_page(step):
    world.page.click_by_id('id-manage-jrf')

@step(u'And When I click Older')
def and_when_i_click_older(step):
    world.page.click_by_id('id-older-jrf')

@step(u'Then I should also see the fourth finalised questionnaire')
def then_i_should_also_see_the_fourth_finalised_questionnaire(step):
    world.page.links_present_by_text(["%s %s" % (world.questionnaire4.name, world.questionnaire4.year)])

@step(u'When I choose to create a new questionnaire')
def when_i_choose_to_create_a_new_questionnaire(step):
    world.page.click_by_id('id-create-new')

@step(u'Then I should see options for selecting a finalized questionnaire and a reporting year')
def then_i_should_see_options_for_selecting_a_finalized_questionnaire_and_a_reporting_year(step):
    world.page.is_text_present('Finalized Questionnaires')
    world.page.is_text_present('Reporting Year')
    world.page.is_element_present_by_id('id_questionnaire')
    world.page.is_element_present_by_id('id_year')

@step(u'When I select a finalized questionnaire and a reporting year')
def when_i_select_a_finalized_questionnaire_and_a_reporting_year(step):
    world.page.select('questionnaire', world.questionnaire1.id)
    world.page.select('year', world.questionnaire1.year+2)

@step(u'And I give it a new name')
def and_i_give_it_a_new_name(step):
    world.page.fill_form({'name': 'Latest Questionnaire'})

@step(u'When I choose to duplicate the questionnaire')
def when_i_choose_to_duplicate_the_questionnaire(step):
    world.page.click_by_id('save-select_survey_wizard')

@step(u'Then I should see a message that the questionnaire was duplicated successfully')
def then_i_should_see_a_message_that_the_questionnaire_was_duplicated_successfully(step):
    world.page.is_element_present_by_css('.alert alert-success')
    world.page.is_text_present('The questionnaire has been duplicated successfully, You can now go ahead and edit it')

@step(u'Then I should see the new questionnaire listed')
def then_i_should_see_the_new_questionnaire_listed(step):
    world.latest_questionnaire = Questionnaire.objects.filter(status=Questionnaire.FINALIZED).latest('created')
    world.page.is_element_present_by_id("questionnaire-%s" % world.latest_questionnaire.id)

@step(u'Then I should a validation error message')
def then_i_should_a_validation_error_message(step):
    world.page.is_element_present_by_css('.error')
    world.page.is_text_present('This field is required.')

@step(u'And I have draft and finalised core questionnaires')
def and_i_have_draft_and_finalised_core_questionnaires(step):
    world.questionnaire1 = Questionnaire.objects.create(name="Questionnaire1", description="Section 1 Description",
                                                        year=2010, status=Questionnaire.FINALIZED)
    Section.objects.create(title="Section1", order=0, questionnaire=world.questionnaire1, name="Section 1 Name")
    world.questionnaire2 = Questionnaire.objects.create(name="Questionnaire2", description="Section 1 Description",
                                                        year=2011, status=Questionnaire.FINALIZED)
    Section.objects.create(title="Section1", order=0, questionnaire=world.questionnaire2, name="Section 1 Name")
    world.questionnaire3 = Questionnaire.objects.create(name="Questionnaire3", description="Section 1 Description",
                                                        year=2012, status=Questionnaire.DRAFT)
    Section.objects.create(title="Section1", order=0, questionnaire=world.questionnaire3, name="Section 1 Name")
    world.questionnaire4 = Questionnaire.objects.create(name="Questionnaire4", description="Section 1 Description",
                                                        year=2013, status=Questionnaire.DRAFT)
    Section.objects.create(title="Section1", order=0, questionnaire=world.questionnaire4, name="Section 1 Name")

@step(u'Then I should see an option to lock each draft Core Questionnaire')
def then_i_should_see_an_option_to_lock_each_draft_core_questionnaire(step):
    assert(world.page.is_element_present_by_id('id-finalize-%s' % world.questionnaire3.id))
    assert(world.page.is_element_present_by_id('id-finalize-%s' % world.questionnaire4.id))

@step(u'And I should see an option to unlock each finalised Core Questionnaire')
def and_i_should_see_an_option_to_unlock_each_finalised_core_questionnaire(step):
    assert(world.page.is_element_present_by_id('id-unfinalize-%s' % world.questionnaire1.id))
    assert(world.page.is_element_present_by_id('id-unfinalize-%s' % world.questionnaire2.id))

@step(u'When I lock a draft Core Questionnaire')
def when_i_lock_a_draft_core_questionnaire(step):
    world.page.click_by_id('id-finalize-%s' % world.questionnaire3.id)

@step(u'Then it should now have an option to unlock it')
def then_it_should_now_have_an_option_to_unlock_it(step):
    world.page.click_by_id('id-unfinalize-%s' % world.questionnaire3.id)

@step(u'When I unlock a finalised Core Questionnaire')
def when_i_unlock_a_finalised_core_questionnaire(step):
    world.page.click_by_id('id-unfinalize-%s' % world.questionnaire1.id)

@step(u'Then it should now have an option to lock it')
def then_it_should_now_have_an_option_to_lock_it(step):
    world.page.click_by_id('id-finalize-%s' % world.questionnaire1.id)

@step(u'When I click on a Draft Core Questionnaire')
def when_i_click_on_a_draft_core_questionnaire(step):
    world.page.click_by_id('questionnaire-%s' % world.questionnaire4.id)

@step(u'Then it should open in an edit view')
def then_it_should_open_in_an_edit_view(step):
    world.page.is_text_present('New Section')
    world.page.is_text_present('New Subsection')

@step(u'I click on a Finalised Core Questionnaire')
def when_i_click_on_a_finalised_core_questionnaire(step):
    world.page.click_by_id('questionnaire-%s' % world.questionnaire2.id)

@step(u'Then it should open in a preview mode')
def then_it_should_open_in_a_preview_mode(step):
    world.page.is_text_present('New Section', status=False)
    world.page.is_text_present('Assign Question', status=False)
    world.page.is_text_present('New Subsection', status=False)

@step(u'And I have two finalised questionnaires')
def and_i_have_two_finalised_questionnaires(step):
    world.questionnaire7 = Questionnaire.objects.create(name="JRF Kampala Test version1", description="description",
                                                        year=2014, status=Questionnaire.FINALIZED)

    Section.objects.create(title="School Based Section1", order=0, questionnaire=world.questionnaire7, name="Name")

    world.questionnaire8 = Questionnaire.objects.create(name="JRF Brazil Test version1", description="description",
                                                        year=2015, status=Questionnaire.FINALIZED)
    Section.objects.create(title="School Section1", order=0, questionnaire=world.questionnaire8, name="Section1 name")

    world.org = Organization.objects.create(name="WHO")
    world.afro = Region.objects.create(name="AFRO", organization=world.org)
    world.amer = Region.objects.create(name="AMER", organization=world.org)
    world.euro = Region.objects.create(name="EURO", organization=world.org)
    world.asia = Region.objects.create(name="ASIA", organization=world.org)

@step(u'And I see finalized questionnaires')
def and_i_see_finalized_questionnaires(step):
    world.page.links_present_by_text(["%s %s" % (world.questionnaire7.name, world.questionnaire7.year),
                                     "%s %s" % (world.questionnaire8.name, world.questionnaire8.year)])
    world.page.is_element_present_by_id('id-unfinalize-%s' % world.questionnaire8.id)

@step(u'Then I should see an option to send to regions on each of the finalized questionnaires')
def then_i_should_see_an_option_to_send_to_regions_on_each_of_the_finalized_questionnaires(step):
    world.page.is_element_present_by_id('id-publish-questionnaire-%s' % world.questionnaire7.id)
    world.page.is_element_present_by_id('id-publish-questionnaire-%s' % world.questionnaire8.id)

@step(u'When I choose option to send core questionnaire to regions')
def when_i_choose_option_to_send_core_questionnaire_to_regions(step):
    world.page.click_by_id('id-publish-questionnaire-%s' % world.questionnaire7.id)

@step(u'Then I should see an interface to choose the regions to which to publish the finalised Core Questionnaire')
def then_i_should_see_an_interface_to_choose_the_regions_to_which_to_publish_the_finalised_core_questionnaire(step):
    world.page.is_text_present("Publish Questionnaire : %s" % world.questionnaire7.name)

@step(u'And I should be able to select one region to which to publish the finalised Core Questionnaire')
def and_i_should_be_able_to_select_one_region_to_which_to_publish_the_finalised_core_questionnaire(step):
    world.page.check("%s" % world.afro.id)
    world.page.click_by_css('button.submit')

@step(u'And I should be able to confirm that the Core Questionnaire is published to the region I selected')
def and_i_should_be_able_to_confirm_that_the_core_questionnaire_is_published_to_the_region_i_selected(step):
    world.page.is_text_present("The questionnaire has been published to %s" % world.afro.name)
    world.page.is_text_present("%s" % world.afro.name)
    world.page.is_element_present_by_id("%s" % world.questionnaire7.id)

@step(u'And I should be able to confirm that the region to which I published the questionnaire is not on the list')
def and_i_should_be_able_to_confirm_that_the_region_to_which_i_published_the_questionnaire_is_not_on_the_list(step):
    world.page.click_by_id('id-publish-questionnaire-%s' % world.questionnaire7.id)
    world.page.is_text_present("%s" % world.afro.name, status=False)

@step(u'And I select two regions to which to publish the finalised Core Questionnaire')
def and_i_select_two_regions_to_which_to_publish_the_finalised_core_questionnaire(step):
    world.page.check(world.amer.id)
    world.page.check(world.asia.id)

@step(u'When I click publish button')
def when_i_click_publish_button(step):
    world.page.click_by_css('.submit')

@step(u'And I should be able to confirm that the Core Questionnaire is published to the regions I selected')
def and_i_should_be_able_to_confirm_that_the_core_questionnaire_is_published_to_the_regions_i_selected(step):
    world.page.is_text_present("The questionnaire has been published to %s, %s" % (world.amer.name, world.asia.name))
    world.page.is_text_present("%s" % world.amer.name)
    world.page.is_text_present("%s" % world.asia.name)

@step(u'And I should be able to confirm that the regions to which I published the questionnaire is not on the list')
def and_i_should_be_able_to_confirm_that_the_regions_to_which_i_published_the_questionnaire_is_not_on_the_list(step):
    world.page.click_by_id('id-publish-questionnaire-%s' % world.questionnaire7.id)
    world.page.is_text_present("%s" % world.amer.name, status=False)
    world.page.is_text_present("%s" % world.asia.name, status=False)