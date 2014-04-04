from questionnaire.models import AnswerGroup, Answer, Questionnaire, Country, Theme


class ExportToTextService:
    HEADERS = "ISO\tCountry\tYear\tField code\tQuestion text\tValue"

    def __init__(self, questionnaires, version=None, countries=None, themes=None):
        self.questionnaires = []
        if questionnaires and isinstance(questionnaires, Questionnaire):
            self.questionnaires.append(questionnaires)
        else:
            self.questionnaires = questionnaires

        self.version = version

        self.countries = []
        if countries and isinstance(countries, Country):
            self.countries.append(countries)
        else:
            self.countries = countries

        self.themes=[]
        if themes and isinstance(themes, Theme):
            self.themes.append(themes)
        else:
            self.themes = themes

    def get_formatted_responses(self):
        formatted_response = [self.HEADERS]
        for questionnaire in self.questionnaires:
            for subsection in questionnaire.sub_sections():
                subsection_answers = self._answers(questionnaire, subsection)
                formatted_response.extend(subsection_answers)

        return formatted_response

    def _answers(self, questionnaire, subsection):
        formatted_response = []
        for group in subsection.parent_question_groups():
            answers_in_group = self._answers_in(questionnaire, group)
            formatted_response.extend(answers_in_group)
        return formatted_response

    def _answer_filter_dict(self, question):
        filter_dict = {'question': question, 'status': Answer.SUBMITTED_STATUS}
        if self.version:
            filter_dict['version'] = self.version
        if self.countries:
            filter_dict['country__in'] = self.countries

        if self.themes:
            filter_dict['question__theme__in'] = self.themes

        return filter_dict

    def _answers_in(self, questionnaire, group):
        formatted_response = []
        ordered_questions = group.ordered_questions()
        primary_question = ordered_questions[0]
        answer_groups = AnswerGroup.objects.filter(grouped_question=group)
        for answer_group in answer_groups:
            answers = answer_group.answer.all().select_subclasses()
            for question in ordered_questions:
                filter_dict = self._answer_filter_dict(question)
                answer = answers.filter(**filter_dict)
                if answer.exists():
                    for answer_ in answer:
                        response_row = self._format_response(questionnaire, answer_, question, primary_question.UID, group, int(answer_group.row))
                        formatted_response.append(response_row)
        return formatted_response

    def _format_response(self, questionnaire, answer, question, primary_question_uid, group, row):
        question_prefix = 'C' if question.is_core else 'R'
        answer_id = "%s_%s_%s_%d" % (question_prefix, primary_question_uid, question.UID, row)
        if question.is_primary:
            primary_question_uid = question.UID
            question_option = ""
            if question.answer_type == 'MultiChoice':
                question_option = answer.response.UID
            answer_id = "%s_%s_%s_%s" % (question_prefix, primary_question_uid, question.UID, question_option)
        question_text_format = "%s | %s | %s" % (group.subsection.section.title, group.subsection.title, question.text)
        answer_format = (answer.country.code, answer.country.name, answer.questionnaire.year, answer_id.encode('base64').strip(),
                         question_text_format, str(answer.response))
        return "%s\t%s\t%s\t%s\t%s\t%s" % answer_format


