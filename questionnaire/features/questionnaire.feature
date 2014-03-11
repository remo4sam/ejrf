Feature: Questionnaire feature
    Scenario: Show questionnaire form
        Given I am logged in as a data submitter
        And I have a questionnaire with sections and subsections
        And I have a question group and questions in that group
        And I set orders for the questions in the group
        And I visit that questionnaires section page
        Then I should see the section title and descriptions
        And I should see the questions
        And I should see the answer fields
        And I should see the instructions

    Scenario: Show questionnaire  group and sub-group
        Given I am logged in as a data submitter
        And I have a questionnaire with sections and subsections
        And I have a question group and questions in that group
        And i have a subgroup with questions in that group
        And I set question orders for the group and subgroup
        And I visit that questionnaires section page
        Then I should see the group title and description
        And I should see the subgroup title and description

    Scenario: Section tabs transition
        Given I am logged in as a data submitter
        And I have a questionnaire with sections and subsections
        And I visit that questionnaires section page
        When I click on a different section tab
        Then I should see that section page

    Scenario: Display additional sub-section on clicking add-more
        Given I am logged in as a data submitter
        And I have a questionnaire with sections and subsections
        And I have a question group and questions in that group
        And I set orders for the questions in the group
        And I visit that questionnaires section page
        Then I should see an Add More button
        When I click the Add More button
        Then I should see a new question group
        When I click the question group delete button
        Then I should not see that question group

