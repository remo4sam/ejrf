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

    def get_answer_status_in(self, questionnaire):
        query_params = {'question__question_group__subsection__section__questionnaire': questionnaire}
        answers = Answer.objects.filter(country=self, **query_params).select_subclasses()
        if answers.exists():
            return AnswerStatus.options[answers.latest('modified').status]
        return AnswerStatus.options[None]