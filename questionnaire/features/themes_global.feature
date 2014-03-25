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
        And I fill in only description
        And I click the save theme button
        Then I should see errors on the form
        When I fill in valid theme details
        And I click the save theme button
        Then I should see the success message
        And I should see the newly created theme in the themes list

    Scenario: Edit Theme
        And I have two themes
        And I visit the themes listing page
        And I click Edit theme button
        And i fill in the theme name
        And I click the update theme button
        Then I should see the update success message
        And I should see the updated theme in the themes list

    Scenario: Global Admin Deletes Theme
        And I have two themes
        And I visit the themes listing page
        And I click Delete theme button
        Then I should see a delete theme confirmation message
        When I confirm the theme deletion
        Then I should see a message that the theme was deleted
        And that theme should no longer appear in the table