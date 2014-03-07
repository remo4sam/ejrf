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