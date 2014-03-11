Feature: Responses
    Background:
        Given I am logged in as a data submitter
        And I have a questionnaire with questions
        And I navigate to the section of the questionnaire to be filled in
        And I enter valid responses to the questions

    Scenario: Save Draft Responses
        When I click the save button
        Then I should see a message that a draft of my responses has been saved
        And when I navigate back to this section
        I should see my responses filled out
        When I enter invalid responses to the questions
        And I click the save button
        Then I should see a save draft error message

    Scenario: Auto-save draft responses on tab transition
        When I switch to another section
        Then I should see a message that a draft of my responses has been saved
        And when I navigate back to this section
        I should see my responses filled out

    Scenario: Data Submitter Submitting Responses
        When I choose to submit my responses
        Then I should see a preview
        And it should contain my responses
        When I choose to submit the responses in the preview
        Then I should see a message that the submission was successful
        And the response fields should be disabled
        And the action for submit should be replaced with edit
        And I should see my submitted responses
        When I select the option to edit my responses
        Then the response fields should be enabled
        When I click the save button
        Then the action for edit should be replaced with submit