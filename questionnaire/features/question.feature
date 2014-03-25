Feature: Questions feature
    Scenario: List questions
        Given I am logged in as a global admin
        And I have 100 questions
        And I visit the question listing page
        Then I should see all questions paginated

    Scenario: Create a simple question
        Given I am logged in as a global admin
        And I have two themes
        And I visit the question listing page
        And I click add new question page
        And I fill in the question details
        And I click save question button
        Then I should see the question created

    Scenario: Create a simple multiChoice question
        Given I am logged in as a global admin
        And I have two themes
        And I visit the question listing page
        And I click add new question page
        And I fill in the multichoice question form data
        And I select Multi-choice answer type
        And I check custom option
        Then I should see the option field
        When Fill in the option
        When I click add more button
        Then I should see another option field
        When I click remove the added option field
        Then I should not see that option field
        And I click save question button
        Then I should see the question created
      
    Scenario: Delete a simple question
        Given I am logged in as a global admin
        And I have two themes
        And I have a question without answers
        And I visit the question listing page
        And I click delete on that question
        Then I should see a delete confirmation modal
        When I confirm delete
        Then I should see that question was deleted successfully

    Scenario: Update Simple Core Question
        Given I am logged in as a global admin
        And I have a core question
        And that core question is used in a questionnaire with submitted responses
        When I visit the question listing page
        And I select the option to edit that question
        The question should be displayed with all its attributes
        When I update the question with invalid details
        I should see an error message
        When I update the question with valid details
        Then I should see a message that the question was successfully updated
        And I should see the updated details
        When I preview the submitted questionnaire where the question was used
        I should see the earlier question display label