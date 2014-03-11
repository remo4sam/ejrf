Feature: Responses
    Scenario: Save Draft Responses
        Given I am logged in as a data submitter
        And I have a questionnaire with questions
        And I navigate to the section of the questionnaire to be filled in
        When I enter valid responses to the questions
        And I click the save button
        Then I should see a message that a draft of my responses has been saved
        And when I navigate back to this section
        I should see my responses filled out
        When I enter invalid responses to the questions
        And I click the save button
        Then I should see a save draft error message

    Scenario: Auto-save draft responses on tab transition
        Given I am logged in as a data submitter
        And I have a questionnaire with questions
        And I navigate to the section of the questionnaire to be filled in
        When I enter valid responses to the questions
        And I switch to another section
        Then I should see a message that a draft of my responses has been saved
        And when I navigate back to this section
        I should see my responses filled out
