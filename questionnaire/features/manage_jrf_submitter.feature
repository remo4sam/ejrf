Feature: Data Submitter Managing JRF
    Scenario: View Questionnaires in Appropriate Category
        Given I am logged in as a data submitter
        And I have a "<questionnaire type>" questionnaire for my region
        When I am viewing the home page
        Then that questionnaire should appear under the list of "<questionnaire type>"  questionnaires
        When I open the "<questionnaire type>" questionnaire for editing
        Then that questionnaire should open in "<questionnaire mode>"
        And uploading attachments should be "<attachment upload status>"

    Examples:
        | questionnaire type  | questionnaire mode | attachment upload status
        | new                 | edit mode          | allowed
        | draft               | edit mode          | allowed
        | submitted           | preview mode       | not allowed