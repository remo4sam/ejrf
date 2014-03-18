Feature: Regional Admin manage eJRF versions
    Scenario: Regional admin manage JRF Versions
        Given I am a Regional Admin
        And I have draft regional questionnaire
        And I have finalized regional questionnaire
        When I login the regional user
        Then I should see the homepage
        And I should see the draft questionnaire
        And  I should see a finalized questionnaire
        When I choose to lock the draft Questionnaire
        Then the questionnaire should be finalised
        When I choose to unlock a finalized questionnaire
        Then the finalized questionnaire should move to the in progress column
        When I click on a draft questionnaire assigned to the region
        Then I should be able to edit it
        When I click on a finalized questionnaire assigned to the region
        Then I should be able to view the questionnaire in preview mode

    Scenario: Regional Admin viewing published regional questionnaire
        Given that I am logged in as a regional admin
        And I have a published regional questionnaire
        When I am viewing the home page
        Then I should see a status that the questionnaire is published
        And there should not be an option to unlock that questionnaire

    Scenario: Data Submitter viewing published regional questionnaire
        Given I am logged in as a data submitter
        When I am viewing the homepage with no published questionnaires for my region
        Then I should see a message that there are no published questionnaires
        When a questionnaire is published for my region
        And I am viewing the homepage
        Then I should now see that published questionnaire