Feature: Viewing status of responses
    Scenario: Global Admin viewing existing regions and countries
        Given I am logged in as a global admin
        And I have regions and countries
        When I am viewing the homepage
        Then I should see the regions listed
        When I select a region in the region list
        Then I should see the countries in that region

    Scenario: Global Admin viewing status by country
        Given I am logged in as a global admin
        And I have regions and countries
        And I have published Questionnaires to a region
        And the data submitters in that region have "<status>"
        When I am viewing the homepage
        And I select that region in the region list
        Then I should see the status of responses for countries in that region as "<result>"

    Examples:
        | status                 | result      |
        | started responding     | In Progress |
        | submitted responses    | Submitted   |
        | not started responding | Not Started |