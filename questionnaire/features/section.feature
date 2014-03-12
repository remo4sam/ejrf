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
    And I click add new section link
    Then I should see a new section modal
    When i fill in the section data
    And I save the regional section
    Then I should see the regional section I created

  Scenario: Delete Regional Section from a regional Questionnaire
    Given I have a Regional Admin
    And I have a questionnaire for my region with sections and subsections
    And I have regional questions already assigned to my questionnaire
    And I login the regional user
    When I open that regional questionnaire for editing
    And I choose to delete one of the section from the questionnaire
    Then I should see a confirmation message
    When I confirm the deletion
    Then I should see a message that the section was deleted
    And the section should no longer appear in the Questionnaire