Feature: Export responses to DEF file

	Background: 
		Given I am registered user	
	    Given I have two countries in a region

	Scenario: Export un filtered text
		And I logged in the user
		And I have a questionnaires
		And I have questions and their answers
	    When I click the extract link
		Then I should see a list of filter options
		Then I should see the export data button
