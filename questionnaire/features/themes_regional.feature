Feature: Regional Themes

  Background:
    Given I am logged in as a regional admin

  Scenario: Create Theme
    And I am on the home page
    Then I should see questions on the top menu
    And I visit the themes listing page
    And I click New Theme button
    When I fill in valid theme details
    And I click the save theme button
    Then I should see the success message
    And I should see the newly created theme in the themes list

  Scenario: Regional Admin Edit Theme
    And I have two themes
    And I visit the themes listing page
    And I click Edit theme button
    And i fill in the theme name
    And I click the update theme button
    Then I should see the update success message
    And I should see the updated theme in the themes list

  Scenario: Regional Admin Deletes Theme
    And I have two themes
    And I visit the themes listing page
    And I click Delete theme button
    Then I should see a delete theme confirmation message
    When I confirm the theme deletion
    Then I should see a message that the theme was deleted
    And that theme should no longer appear in the table