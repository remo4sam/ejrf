Feature: Regional Questions
    Scenario: Regional Admin deleting questions from Question Bank
        Given that I am logged in as a regional admin
        And I have regional questions in the question bank
        And I have two themes
        When I navigate to the question bank
        Then I should see an option to delete each question
        When I choose to delete a question
        Then I should see a prompt to confirm deleting the question
        When I confirm the regional question deletion
        Then that question should not appear in the Question bank
        And I should see a message that the regional question was deleted

    Scenario: Regional Admin Creating Simple Question
        Given that I am logged in as a regional admin
        And I have two themes
        And I visit the question listing page
        And I click add new question page
        And I fill in the question details
        And I click save question button
        Then I should see the question created

    Scenario: Regional Admin Creating Simple MultiChoice Question
        Given that I am logged in as a regional admin
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