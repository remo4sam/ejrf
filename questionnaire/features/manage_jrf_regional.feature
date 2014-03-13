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





