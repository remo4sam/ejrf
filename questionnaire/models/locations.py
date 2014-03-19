from django.db import models
from questionnaire.models import Answer
from questionnaire.models.answers import AnswerStatus
from questionnaire.models.base import BaseModel


class Organization(BaseModel):
    name = models.CharField(max_length=100, blank=False, null=True)

    def __unicode__(self):
        return "%s" % self.name


class Location(BaseModel):
    name = models.CharField(max_length=100, blank=False, null=True)

    class Meta:
        abstract = True
        app_label = 'questionnaire'

    def __unicode__(self):
        return "%s" % self.name


class Region(Location):
    description = models.CharField(max_length=300, blank=True, null=True)
    organization = models.ForeignKey(Organization, blank=False, null=True, related_name="regions")


class Country(Location):
    regions = models.ManyToManyField(Region, blank=False, null=True, related_name="countries")
    code = models.CharField(max_length=5, blank=False, null=True)

    def answer_status(self):
        answers = Answer.objects.filter(country=self).select_subclasses()
        if answers.exists():
            return AnswerStatus.options[answers.latest('modified').status]
        return AnswerStatus.options[None]

    def data_submitter(self):
        data_submitter_name_question = "Name of person in Ministry of Health"
        submitter_answer = Answer.objects.filter(country=self, question__text__contains=data_submitter_name_question).latest('modified')
        if submitter_answer:
            return submitter_answer.textanswer.response

    def all_versions(self, questionnaire=None):
        query_params = {'question__question_group__subsection__section__questionnaire__region__countries': self,
                        'question__question_group__subsection__section__questionnaire__status': 'published'}
        all_answers = Answer.objects.select_subclasses()
        answers = all_answers.filter(country=self, **query_params)
        if questionnaire:
            answers = all_answers.filter(country=self, question__question_group__subsection__section__questionnaire=questionnaire)
            return {questionnaire: list(set(answers.values_list('version', flat=True)))}
        return list(set(answers.values_list('version', flat=True)))

    def get_versions_for(self, questionnaires):
        questionnaire_version_map = {}
        for questionnaire in questionnaires:
            questionnaire_version_map.update(self.all_versions(questionnaire))
        return questionnaire_version_map