Feature: Section feature
    Scenario: Create a section
        Given I am logged in as a global admin
        And I have a questionnaire with sections and subsections
        And I visit that questionnaires section page
        And I click add new section link
        Then I should see a new section modal
        When i fill in the section data
        And I save the section
        Then I should see the section I created

    Scenario: Create section with form errors
        Given I am logged in as a global admin
        And I have a questionnaire with sections and subsections
        And I visit that questionnaires section page
        And I click add new section link
        Then I should see a new section modal
        And I fill in invalid data
        And I save the section
        Then I should see error messages against the fields

<<<<<<< HEAD
    Scenario: Update Section in Core Questionnaire
        Given I am logged in as a global admin
        And I have a questionnaire with sections and subsections
        And I visit that questionnaires section page
        And I choose to update a section
        Then I should see an edit section modal
        When I update the section details
        And I save the changes to the section
        Then I should see a message that the section was updated
        And I should see the changes I made to the section in the questionnaire
=======
    Scenario: Delete a Section
        Given I am logged in as a global admin
        And I have a questionnaire with sections and with subsections
        When I open that questionnaire for editing
        And I choose to delete a section
        Then I should see a confirmation dialog
        When I confirm that I want to delete
        Then I should see a message that the section was deleted
>>>>>>> [Robert, Tom, Emily] Added funtional tests for the delete section story
