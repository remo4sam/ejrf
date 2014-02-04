Feature: Responses
    Scenario: Save Draft Responses
        Given I am a logged-in user with a user Profile
        And I have a questionnaire with questions
        And I navigate to the section of the questionnaire to be filled in
        When I enter valid responses to the questions
        And I click the save button
        Then I should see a message that a draft of my responses has been saved
        When I enter invalid responses to the questions
        And I click the save button
        Then I should see a save draft error message