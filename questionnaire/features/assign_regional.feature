Feature: Regional Admin Assigning Questions
    Background:
        Given I am a Regional Admin
        And I have a questionnaire for my region with sections and subsections
        And I have regional questions already assigned to my questionnaire
        And I have regional questions that are not assigned to my questionnaire
        And I login the regional user

    Scenario: Regional Admin Assign Questions to questionnaire
        When I open that regional questionnaire for editing
        And I choose to assign a question to a sub-section
        When I select the regional questions to assign to the questionnaire
        And I click done button
        Then I should see the newly assigned regional questions in the questionnaire
        And the regional question numbers should be prefixed with the region name

    Scenario: Regional Admin Unassign Questions from questionnaire
        And I have core questions assigned to my questionnaire
        When I open that regional questionnaire for editing
        Then I should see unassign options for each regional question
        And I should not see unassign options for the core questions
        When I choose to unassign a question from a sub-section
        Then I should see a prompt to confirm unassign of the question
        When I confirm unassign of the question
        Then the unassigned question should not appear in the questionnaire
        And I should see a message that question is successfully unassigned
        And the question numbering should be updated

