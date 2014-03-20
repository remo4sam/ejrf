from django.db import models
from questionnaire.models.base import BaseModel


class Theme(BaseModel):
    name = models.TextField("Name", max_length=100, blank=False, null=False)
    description = models.TextField("Description", max_length=500, blank=True, null=True)