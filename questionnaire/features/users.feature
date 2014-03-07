Feature: User management
    Scenario: User login
        Given I am registered user
        And I visit the login page
        And I fill in the login credentials
        And I submit the form
        Then I should be redirected home page
        And I should see my username and the logout link
        When I click the logout link
        Then I should see the login page again

    Scenario: User login with invalid credentials
        Given I visit the login page
        And I fill in invalid user credentials
        And I submit the form
        Then I should see an error message

    Scenario: User accessing extract page without logging in
        Given I visit the extract page
        When I fill in the login credentials
        Then I should see the extract page

    Scenario: List users
        Given I have a global admin user
        And I have 100 other users
        And I logged in the user
        And I visit the user listing page
        Then I should see the list of users paginated

    Scenario: Filter users list
        Given I have a global admin user
        And I logged in the user
        And I have a region
        And I have 10 users in one of the regions
        And I have five others not in that region
        And I visit the user listing page
        And I select a region
        And I click get list
        Then I should see only the users in that region

    Scenario: Create a global admin user
        Given I have a global admin user
        And I have 100 other users
        And I logged in the user
        And I visit the user listing page
        And I click an new user button
        And I fill in the user information
        And I select global admin role
        And I click the create button
        Then I should see that the user was successfully created
        And I should see the user listed on the listing page

    Scenario: Create a regional admin user
        Given I have a global admin user
        And I have one region, in an organization
        And I logged in the user
        And I have 10 users in one of the regions
        And I have roles
        And I visit the user listing page
        And I click an new user button
        And I fill in the user information
        And I select regional admin role
        Then I should see only organization and region fields
        When I select the organization
        And I select the region for the new user
        And I click the create button
        Then I should see that the data regional admin was successfully created

    Scenario: Create a data submitter user
        Given I have a global admin user
        And I have one region, in an organization
        And I have a countries in that region
        And I logged in the user
        And I have roles
        And I visit the user listing page
        And I click an new user button
        And I fill in data submitter information
        And I select data submitter role
        When I select a country
        And I click the create button
        Then I should see that the data submitter was successfully created

    Scenario: Filter users list by organization, region and role
        Given I have a global admin user
        And I have two organizations, region and role
        And I have 4 users in the UNICEF organization, 2 of which are regional admins in the AFRO region
        And I have 2 users in the WHO organization
        And I logged in the user
        And I visit the user listing page
        When I select UNICEF organization
        And I select the AFRO region and regional admin role
        And I click get list
        Then I should see only regional admin users in the UNICEF organization in the AFRO region
        And I should not see the rest of the users

    Scenario: Filter users by regions and organizations
        Given I have a global admin user
        And I logged in the user
        And I have two organizations, region and role
        And I have 4 users in the UNICEF organization, 2 of which are regional admins in the AFRO region
        And I have countries in AFRO region
        And I have four roles
        And I have 2 country admins and data submitters in countries in the AFRO
        And I visit the user listing page
        When I select UNICEF organization
        And I select the AFRO region
        And I click get list
        Then I should see only regional admin users in the UNICEF organization in the AFRO region
        Then I should see all the data submitters too
        And I should not see the rest of the users


    Scenario: Get regions for selected organizations
        Given I have a global admin user
        And I have two organizations, region and role
        And I logged in the user
        And I visit the user listing page
        And I select unicef
        Then I should see the region under unicef in the select
        And I should not see the region under who in the select

    Scenario: Create user organisation and region options
        Given I have a global admin user
        And I have two organizations and regions
        And I have four roles
        And I logged in the user
        And I visit the user listing page
        And I click an new user button
        When I select the global admin role
        Then I should see organisations drop down
        When I select the region admin role
        Then I should see region and country
        When I select the country admin role
        Then I should see country drop down
        When I select the data submitter role
        Then I should see country drop down

    Scenario: Global Admin Disables a User Account
        Given I am a logged-in Global Admin
        And I have a an active data submitter user
        And I visit the user listing page
        And I select that user
        And I make that user inactive
        Then that user should be unable to log in
        And they should see a message that their account is inactive when they try to log in