Feature: Subsection feature
    Scenario: Create a subsection
        Given I am logged in as a global admin
        And I have a questionnaire with sections and subsections
        And I visit that questionnaires section page
        And I click add new subsection link
        Then I should see a new subsection modal
        When i fill in the subsection data
        And I save the subsection
        Then I should see the subsection I just created

    Scenario: Update Subsection in Core Questionnaire
        Given I am logged in as a global admin
        And I have a questionnaire with sections and subsections
        And I visit that questionnaires section page
        And I choose to update a subsection
        Then I should see an edit subsection modal
        When I update the subsection details
        And I save the changes to the subsection
        Then I should see a message that the subsection was updated
        And I should see the changes I made to the subsection in the questionnaire

    Scenario: Delete Regional Subsection from a regional Questionnaire
        Given I am a Regional Admin
        And I have a questionnaire for my region with sections and subsections
        And I have regional questions already assigned to my questionnaire
        And I login the regional user
        When I open that regional questionnaire for editing
        And I choose to delete one of the sub sections from the questionnaire
        Then I should see a delete subsection confirmation message
        When I confirm my intention to delete that subsection
        Then I should see a message that the sub-section was deleted
        And the sub section should no longer appear in the Questionnaire

    Scenario: Create Regional subsection
        Given I am a Regional Admin
        And I have a questionnaire for my region with sections and subsections
        And I have regional questions already assigned to my questionnaire
        And I login the regional user
        When I open that regional questionnaire for editing
        And I click add new subsection link
        Then I should see a new subsection modal
        When i fill in the subsection data
        And I save the subsection
        Then I should see the subsection I just created

    Scenario: Update Subsection in Regional Questionnaire
        Given that I am logged in as a regional admin
        And I have a questionnaire in a region with sections and subsections
        And I visit that questionnaires section page
        Then I should not see core subsection edit link
        When I click the edit link for regional subsection
        Then I should see an edit subsection modal
        When I update the subsection details
        And I save the changes to the subsection
        Then I should see a success message that the subsection was updated
        And I should see those changes to the regional subsection in the questionnaire