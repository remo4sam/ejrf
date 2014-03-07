from django.db import models
from questionnaire.models.base import BaseModel
from questionnaire.utils.model_utils import largest_uid, stringify


class Question(BaseModel):

    NUMBER = "Number"
    MULTICHOICE = "MultiChoice"
    ANSWER_TYPES = (
        ("Date", "Date"),
        ("MultiChoice", MULTICHOICE),
        ("Number", NUMBER),
        ("Text", "Text"),
    )

    text = models.TextField(blank=False, null=False)
    export_label = models.TextField(blank=True, null=False)
    instructions = models.TextField(blank=True, null=True)
    UID = models.CharField(blank=False, null=False, max_length=6, unique=True)
    answer_type = models.CharField(blank=False, null=False, max_length=20, choices=ANSWER_TYPES)
    region = models.ForeignKey("Region", blank=False, null=True, related_name="questions")
    is_primary = models.BooleanField(blank=False, null=False, default=False)
    is_required = models.BooleanField(blank=False, null=False, default=False)

    def all_answers(self):
        return self.answers.filter(status='Submitted').order_by('answergroup__id').select_subclasses()

    @property
    def is_core(self):
        return not self.region

    def __unicode__(self):
        return "%s" % self.text

    def group(self):
        return self.question_group.all()[0]

    def is_first_in_group(self):
        questions = self.group().ordered_questions()
        return self == questions[0]

    def is_last_in_group(self):
        questions = self.group().ordered_questions()
        return self == questions[-1]

    def has_question_option_instructions(self):
        return self.options.exclude(instructions=None)

    def latest_answer(self, parent_group, country, version=1):
        answer = self.answers.filter(answergroup__grouped_question=parent_group,
                                     country=country, version=version).select_subclasses()
        if answer.exists():
            return answer.latest('modified')
        return None

    def is_in_subgroup(self):
        return self.question_group.exclude(parent=None).exists()

    def can_be_deleted(self):
        return not self.all_answers().exists()

    def get_option_at(self, index=1):
        if self.is_primary:
            all_options = self.options.order_by('text')
            return all_options[index - 1]

    def is_assigned_to(self, questionnaire):
        return self.question_group.filter(subsection__section__questionnaire=questionnaire).exists()

    @classmethod
    def next_uid(cls):
        return stringify(largest_uid(cls) + 1)


class QuestionOption(BaseModel):
    text = models.CharField(max_length=100, blank=False, null=False)
    question = models.ForeignKey(Question, related_name="options")
    instructions = models.TextField(blank=True, null=True)
    UID = models.CharField(blank=False, max_length=6, unique=True, null=True)

    def __unicode__(self):
        return "%s" % self.text

    class Meta:
        ordering = ('modified',)
        app_label = 'questionnaire'