Feature: Themes
  Background:
    Given I am logged in as a global admin

  Scenario: List themes
    Given I have 100 themes
    And I visit the themes listing page
    Then I should see 2 of the themes

  Scenario: Create theme
    And I visit the themes listing page
    And I click New Theme button
    And I fill in theme details form
    And I click the save theme button
    Then I should see the success message
    And I should see the newly created theme in the themes list