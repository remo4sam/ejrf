Feature: Preview
    Scenario: Data submitter previewing responses
        Given I am logged in as a data submitter
        And I have a questionnaire with questions
        And I navigate to the section of the questionnaire to be filled in
        When I enter valid responses to the questions
        And I choose to preview my responses
        Then I should see a preview layout of my responses
        And it should contain my responses
        #And the response fields in the preview should be inactive
        And there should be a provision for me to submit my responses
        And there should be a provision for me to exit the preview
        When I choose to exit the responses preview
        Then I should see my questionnaire again with options for saving
        #And the response fields should now be active

    Scenario: Global Admin previewing a Core Questionnaire
        Given I am a logged-in Global Admin
        And I have a questionnaire with sections and with subsections
        And I have assigned questions
        When I open that questionnaire for editing
        Then I should be able to see an option to preview the questionnaire
        When I choose the option to preview the questionnaire
        Then I should see a preview layout of my questionnaire
        And I should see all my assigned questions in the preview
        #And the response fields should be active
        When I choose to exit the questionnaire preview
        Then I should see my questionnaire again with options for editing