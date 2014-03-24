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
        And the option to show versions for countries in that region should be "<view versions status>"

    Examples:
        | status                 | result      | view versions status |
        | started responding     | In Progress | not visible          |
        | submitted responses    | Submitted   | visible              |
        | not started responding | Not Started | not visible          |

    Scenario: Global Admin extracts data and previews a questionnaire while viewing global status
        Given I am logged in as a global admin
        And I have regions and countries
        And I have published Questionnaires to a region
        And a data submitter from a country in that region has submitted multiple versions
        When I am viewing the homepage
        And I select that region in the region list
        And I select the option to view submitted versions for that country
        Then I should see options to extract and preview the questionnaire for each submitted version
        When I select the option to preview a submitted version
        Then I should see that submitted questionnaire version in preview mode
        And the questionnaire should contain that versions responses