from time import sleep
from lettuce import step, world
from questionnaire.features.pages.home import HomePage
from questionnaire.features.pages.manage import ManageJrfPage
from questionnaire.models import Questionnaire, Section, SubSection


@step(u'And I have draft regional questionnaire')
def and_i_have_draft_regional_questionnaire(step):
    world.questionnaire_created = Questionnaire.objects.create(name="JRF Questionnaire Created",
                                                               description="Description",
                                                               year=2013, status=Questionnaire.DRAFT,
                                                               region=world.region)
    world.first_section = Section.objects.create(order=0, title="WHO/UNICEF Section-Created",
                                                 questionnaire=world.questionnaire_created, name="Section One",
                                                 region=world.region)
    world.second_section = Section.objects.create(order=1, title="Another title",
                                                  description="This is just another one of them",
                                                  questionnaire=world.questionnaire_created, name="Section Two",
                                                  region=world.region)
    world.first_sub_section = SubSection.objects.create(order=1, section=world.first_section, region=world.region)


@step(u'And I have finalized regional questionnaire')
def and_i_have_finalized_regional_questionnaire(step):
    world.finalized_questionnaire = Questionnaire.objects.create(name="JRF Questionnaire-Finalized",
                                                                 description="Description",
                                                                 year=2013, status=Questionnaire.FINALIZED,
                                                                 region=world.region)
    world.first_section_finalized = Section.objects.create(order=0, title="WHO/UNICEF Finalized Section",
                                                           questionnaire=world.finalized_questionnaire,
                                                           name="Section One", region=world.region)
    world.second_section_finalized = Section.objects.create(order=1, title="Another title",
                                                            description="This is just another one of them",
                                                            questionnaire=world.finalized_questionnaire,
                                                            name="Section Two", region=world.region)
    world.first_sub_section_finalized = SubSection.objects.create(order=1, section=world.first_section_finalized,
                                                                  region=world.region)


@step(u'Then I should see the homepage')
def then_i_should_see_the_homepage(step):
    world.page.is_text_present("%s Questionnaire Templates" % world.region)
    world.page.is_text_present("In Progress")
    world.page.is_text_present("Finalized")


@step(u'And I should see the draft questionnaire')
def and_i_should_see_the_draft_questionnaire(step):
    world.page.is_text_present(world.questionnaire_created.name)


@step(u'And  I should see a finalized questionnaire')
def and_i_should_see_a_finalized_questionnaire(step):
    world.page.is_text_present(world.finalized_questionnaire.name)


@step(u'When I choose to lock the draft Questionnaire')
def when_i_choose_to_lock_the_draft_questionnaire(step):
    world.page.click_by_id('id-finalize-%s' % world.questionnaire_created.id)


@step(u'Then the questionnaire should be finalised')
def then_the_questionnaire_should_be_finalised(step):
    world.page.is_text_present('The questionnaire has been finalized successfully')
    assert world.page.is_element_present_by_id('id-finalized-questionnaire-%s' % world.questionnaire_created.id)


@step(u'When I choose to unlock a finalized questionnaire')
def when_i_choose_to_unlock_a_finalized_questionnaire(step):
    world.page.click_by_id("id-unfinalize-%s" % world.finalized_questionnaire.id)


@step(u'Then the finalized questionnaire should move to the in progress column')
def then_the_finalized_questionnaire_should_move_to_the_in_progress_column(step):
    world.page.is_text_present('The questionnaire is now in progress')
    assert world.page.is_element_present_by_id("questionnaire-%s" % world.finalized_questionnaire.id)


@step(u'When I click on a draft questionnaire assigned to the region')
def when_i_click_on_a_draft_questionnaire_assigned_to_the_region(step):
    world.page.click_by_id("questionnaire-%d" % world.finalized_questionnaire.id)


@step(u'Then I should be able to edit it')
def then_i_should_be_able_to_edit_it(step):
    assert world.page.is_element_present_by_id("new-subsection")
    assert world.page.is_element_present_by_id("id-assign-%s" % world.first_sub_section_finalized.id)


@step(u'When I click on a finalized questionnaire assigned to the region')
def when_i_click_on_a_finalized_questionnaire_assigned_to_the_region(step):
    world.page = HomePage(world.browser)
    world.page.visit()
    world.page.click_by_id("id-finalized-questionnaire-%s" % world.questionnaire_created.id)


@step(u'Then I should be able to view the questionnaire in preview mode')
def then_i_should_be_able_to_view_the_questionnaire_in_preview_mode(step):
    assert world.page.is_element_not_present_by_id("id-assign-%s" % world.first_sub_section_finalized.id)


@step(u'And I have a published regional questionnaire')
def and_i_have_a_published_regional_questionnaire(step):
    world.published_regional_questionnaire = Questionnaire.objects.create(name="JRF Finalised Regional",
                                                                          description="Description",
                                                                          year=2014, status=Questionnaire.PUBLISHED,
                                                                          region=world.region)


    world.regional_section = Section.objects.create(order=0, title="JRF Published Questionnaire", description="Description",
                                                questionnaire=world.published_regional_questionnaire,
                                                name="Cover page")
    world.regional_subsection = SubSection.objects.create(order=1, section=world.regional_section)


@step(u'When I am viewing the home page')
def when_i_am_viewing_the_home_page(step):
    world.page = HomePage(world.browser)
    world.page.visit()


@step(u'Then I should see a status that the questionnaire is published')
def then_i_should_see_a_status_that_the_questionnaire_is_published(step):
    world.page.is_text_present('Published')


@step(u'And there should not be an option to unlock that questionnaire')
def and_there_should_not_be_an_option_to_unlock_that_questionnaire(step):
    assert world.page.is_element_not_present_by_id('id-unfinalize-%s' % world.published_regional_questionnaire.id)



@step(u'When a questionnaire is published for my region')
def when_a_questionnaire_is_published_for_my_region(step):
    world.finalised_regional_questionnaire = Questionnaire.objects.create(name="JRF Published Questionnaire",
                                                                          description="Custom Description",
                                                                          year=2014, status=Questionnaire.PUBLISHED,
                                                                          region=world.region)
    world.regional_section = Section.objects.create(order=0, title="JRF Published Questionnaire",
                                                    description="Description",
                                                    questionnaire=world.finalised_regional_questionnaire,
                                                    name="Cover page")
    world.regional_subsection = SubSection.objects.create(order=1, section=world.regional_section)


@step(u'And I am viewing the homepage')
def and_i_viewing_the_homepage(step):
    step.given('When I am viewing the home page')


@step(u'Then I should now see that published questionnaire')
def then_i_should_now_see_that_published_questionnaire(step):
    world.page.is_text_present('JRF Published Questionnaire')


@step(u'And I click finalize my regional questionnaire')
def and_i_click_finalize_my_regional_questionnaire(step):
    world.page.click_by_id("id-finalize-%s" % world.questionnaire.id)


@step(u'Then I should see that the questionnaire was sent to the global admin successfully')
def then_i_should_see_that_the_questionnaire_was_sent_to_the_global_admin_successfully(step):
    world.page.is_text_present("The questionnaire has been finalized successfully.")
    world.page = ManageJrfPage(world.browser)


@step(u'And I should not see the lock icon any more')
def and_i_should_not_see_the_lock_icon_any_more(step):
    world.page.validate_icon_present("id-finalize-%s" % world.questionnaire.id, status=False)


@step(u'And I should see the unlock icon')
def and_i_should_see_the_unlock_icon(step):
    world.page.validate_icon_present("id-unfinalize-%s" % world.questionnaire.id)
