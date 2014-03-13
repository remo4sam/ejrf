from lettuce import step, world
from questionnaire.features.pages.home import HomePage
from questionnaire.features.pages.step_utils import assign, create_user_with_no_permissions
from questionnaire.features.pages.users import LoginPage
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
    assert world.page.is_element_present_by_id('id-finalized-questionnaire-%s' % world.questionnaire_created.id)


@step(u'When I choose to unlock a finalized questionnaire')
def when_i_choose_to_unlock_a_finalized_questionnaire(step):
    world.page.click_by_id("id-unfinalize-%s" % world.finalized_questionnaire.id)


@step(u'Then the finalized questionnaire should move to the in progress column')
def then_the_finalized_questionnaire_should_move_to_the_in_progress_column(step):
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
