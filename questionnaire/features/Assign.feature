Feature: Assigning Questions

    Scenario: Assign Questions to Questionnaire from within Questionnaire
        Given I am a logged-in Global Admin
        And I have a questionnaire with sections and with subsections
        And I have assigned questions
        And I have unassigned questions
        When I open that questionnaire for editing
        Then I should see options to assign questions to sub-sections
        When I choose to assign a question to a sub-section
        Then I should see the question bank with both assigned and unassigned questions
        When I select questions to assign to the questionnaire
        Then I should see the newly assigned questions in the questionnaire when I am done editing

    Scenario: Unassign Questions from Questionnaire
        Given I am a logged-in Global Admin
        And I have a questionnaire with sections and with subsections
        And I have assigned questions
        When I open that questionnaire for editing
        Then I should see options for unassigning questions from the questionnaire
        When I choose to unassign a question from the questionnaire
        And I confirm my actions
        Then I should see a message that the question was unassigned
        And that question should no longer appear in the questionnaire

    Scenario: Regional Admin Assign Questions to questionnaire
        Given I am a logged-in as a Regional Admin
        And I have a questionnaire for my region with sections and subsections
        And I have regional questions already assigned to my questionnaire
        And I have regional questions that are not assigned to my questionnaire
        And I login the regional user
        When I open that regional questionnaire for editing
        And I choose to assign a question to a sub-section
        When I select the regional questions to assign to the questionnaire
        And I click done button
        Then I should see the newly assigned regional questions in the questionnaire