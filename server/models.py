from django.db import models
from unrest.models import JsonModel


class AbstractModel(JsonModel):
    class Meta:
        abstract = True
    json_fields = ['id', 'data']

    def __str__(self):
        return self.data.get(
            "name",
            "{} #: {}".format(self.__class__.__name__, self.id)
        )


class PartyImage(JsonModel):
    pass


class SourceImage(models.Model):
    name = models.CharField(max_length=32)
    src = models.ImageField(upload_to="source_images")
    @property
    def as_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'src': self.src.url,
        }
    def __str__(self):
        return self.name