Feature: Regional Questions
    Scenario: Regional Admin deleting questions from Question Bank
        Given that I am logged in as a regional admin
        And I have regional questions in the question bank
        When I navigate to the question bank
        Then I should see an option to delete each question
        When I choose to delete a question
        Then I should see a prompt to confirm deleting the question
        When I confirm the regional question deletion
        Then that question should not appear in the Question bank
        And I should see a message that the regional question was deleted