from model_utils import Choices
from model_utils.fields import StatusField
from questionnaire.models.base import BaseModel
from django.db import models
from questionnaire.models import Region
from django.core.urlresolvers import reverse


class Questionnaire(BaseModel):
    DRAFT = 'draft'
    PUBLISHED = 'published'
    FINALIZED = 'finalized'
    STATUS = Choices(FINALIZED, PUBLISHED, DRAFT)
    name = models.CharField(max_length=256, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    status = StatusField(choices_name="STATUS", default=DRAFT)
    region = models.ForeignKey(Region, blank=True, null=True, related_name="questionnaire")

    def __unicode__(self):
        return '%s' % self.name

    def sub_sections(self):
        sections = self.sections.all()
        from questionnaire.models import SubSection
        return SubSection.objects.filter(section__in=sections)

    def get_all_questions(self):
        all_questions = []
        for subsection in self.sub_sections():
            all_questions.extend(subsection.all_questions())
        return all_questions

    def all_groups(self):
        all_groups = []
        for subsection in self.sub_sections():
            all_groups.extend(subsection.question_group.all())
        return all_groups

    def is_finalized(self):
        return self.status == Questionnaire.FINALIZED

    def is_published(self):
        return self.status == Questionnaire.PUBLISHED

    def absolute_url(self):
        args = self.id, self.first_section().id
        return reverse('questionnaire_entry_page', args=args)

    def first_section(self):
        return self.sections.order_by('order')[0]

    def has_more_than_one_section(self):
        return self.sections.all().count() > 1