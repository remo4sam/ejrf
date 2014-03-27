Feature: Data Submitter Managing JRF
    Scenario: View Questionnaires in Appropriate Category
        Given I am logged in as a data submitter
        And I have a "<questionnaire type>" questionnaire for my region
        When I am viewing the home page
        Then that questionnaire should appear under the list of "<questionnaire type>"  questionnaires
        When I open the "<questionnaire type>" questionnaire for editing
        Then that questionnaire should open in "<questionnaire mode>"

    Examples:
        | questionnaire type  | questionnaire mode |
        | new                 | edit mode          |
        | draft               | edit mode          |
        | submitted           | preview mode       |