Feature: Global Admin home
    Scenario: View Versions
        Given I two have regions and three countries in those regions
        Given I have a questionnaire published one of the regions
        And one of the countries in that region has  two versions of answers for the questionnaire
        Given I am logged in as a global admin
        When I expand that region
        Then I should see the country with started status
        And when I click the country
        Then I should see its versions listed under it
        When I click on version 1
        Then I should see the submitted answers in a modal