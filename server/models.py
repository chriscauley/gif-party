from django.contrib.postgres.fields import JSONField
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
    @property
    def as_json(self):
        return {
            **self.data,
            'id': self.id,
        }

    @property
    def sourceimage(self):
        if not hasattr(self,'_sourceimage'):
            self._sourceimage = SourceImage.objects.get(id=self.data['source'])
        return self._sourceimage

    def save(self,*args,**kwargs):
        self.refresh()
        return super(PartyImage,self).save(*args,**kwargs)

    def refresh(self):
        print(self.short_args,self.args)

    @property
    def args(self):
        args = []
        if self.data.get('resize'):
            args += ['-r',self.data['resize']]
        if self.data.get('negate'):
            args += ['-N',self.data['negate']]
        if self.data.get('n_frames'):
            args += ['-n',self.data['n_frames']]
        return args

    @property
    def short_args(self):
        return "".join([str(arg) for arg in self.args])


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