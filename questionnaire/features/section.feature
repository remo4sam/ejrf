Feature: Section feature

  Scenario: Create a section
    Given I am logged in as a global admin
    And I have a questionnaire with sections and subsections
    And I visit that questionnaires section page
    And I click add new section link
    Then I should see a new section modal
    When i fill in the section data
    And I save the section
    Then I should see the section I created

  Scenario: Create section with form errors
    Given I am logged in as a global admin
    And I have a questionnaire with sections and subsections
    And I visit that questionnaires section page
    And I click add new section link
    Then I should see a new section modal
    And I fill in invalid data
    And I save the section
    Then I should see error messages against the fields

  Scenario: Update Section in Core Questionnaire
    Given I am logged in as a global admin
    And I have a questionnaire with sections and subsections
    And I visit that questionnaires section page
    And I choose to update a section
    Then I should see an edit section modal
    When I update the section details
    And I save the changes to the section
    Then I should see a message that the section was updated
    And I should see the changes I made to the section in the questionnaire

  Scenario: Delete Section in Core Questionnaire
    Given I am logged in as a global admin
    And I have a questionnaire with sections and subsections
    And I visit that questionnaires section page
    Then I should see an option to delete each section
    When I choose to delete a section
    Then I should see a confirmation message
    When I confirm the deletion
    Then I should see a message that the section was deleted
    And the section should no longer appear in the Questionnaire
    And the section numbering should be updated

  Scenario: Create a Regional Section
    Given I am logged in as a regional admin
    And I have a regional questionnaire with sections and subsections
    And I visit that questionnaires section page
    Then I should see an option to add a new regional section
    When I click add new section link
    Then I should see a new section modal
    When i fill in the section data
    And I save the regional section
    Then I should see the regional section I created
    And its name and title should be prefixed with the region name

  Scenario: Delete Regional Section from a regional Questionnaire
    Given that I am logged in as a regional admin
    And I have a questionnaire for my region with sections and subsections
    And I have regional questions already assigned to my questionnaire
    And I am viewing the manage regional JRF page
    When I open that regional questionnaire for editing
    Then I should see options to delete the regional sections
    When I choose to delete one of the regional sections
    Then I should see a confirmation message
    When I confirm the regional section deletion
    Then I should see a message that the section was deleted
    And the regional section should no longer appear in the Questionnaire
    And the numbering of the remaining sections should be updated

  Scenario: Update Section in Regional Questionnaire
    Given that I am logged in as a regional admin
    And I have a questionnaire for my region with sections and subsections
    And I visit that questionnaires section page
    Then I should not see edit icon for core sections
    And I should see an option to edit regional sections
    When I choose to update a section
    Then I should see an edit section modal
    When I update the section details
    And I save the changes to the section
    Then I should see a message that the section was updated
    And I should see the changes I made to the regional section in the questionnaire