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