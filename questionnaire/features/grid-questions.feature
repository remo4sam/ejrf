Feature: Grid questions display all
    Background:
        Given I am logged in as a data submitter
        And I have a questionnaire with sections and subsections
        And I have a grid group with all options of the primary question showable
        And I have 3 questions in that group one of which is primary
        And I have a sub group in that group with two questions
        And I visit that questionnaires section page

    Scenario: Display grid with all options shown
        Then I should see that grid with all the options of the primary question shown

    Scenario: Response to Grid -- Success
        When I respond the questions
        And I click the save button
        Then I should see a message that a draft of my responses has been saved
        I should see my responses filled out

