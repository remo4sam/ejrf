Feature: Global Admin Assigning Questions
    Background:
        Given I am a logged-in Global Admin
        And I have a questionnaire with sections and with subsections
        And I have assigned questions
        And I have unassigned questions
        When I open that questionnaire for editing

    Scenario: Assign Questions to Questionnaire from within Questionnaire
        Then I should see options to assign questions to sub-sections
        When I choose to assign a question to a sub-section
        Then I should see the question bank with both assigned and unassigned questions
        And I should see an option to hide already assigned questions
        When I select the option to hide already assigned questions
        Then I should only see the unassigned questions in the question bank
        And I should not see the assigned questions in the question bank
        When I select questions to assign to the questionnaire
        Then I should see the newly assigned questions in the questionnaire when I am done editing

    Scenario: Unassign Questions from Questionnaire
        Then I should see options for unassigning questions from the questionnaire
        When I choose to unassign a question from the questionnaire
        And I confirm my actions
        Then I should see a message that the question was unassigned
        And that question should no longer appear in the questionnaire