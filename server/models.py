from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from subprocess import Popen, PIPE

import os
import json

from unrest.models import BaseModel
from party import utils

_choices = lambda a: tuple(zip(a, a))
_delay_choices = lambda a: tuple(zip(a, [f'{int(100/i):d} fps' for i in a]))

class PartyImage(BaseModel):
    RESIZE_CHOICES = ((0,'No Resize'),) + _choices([32, 64, 128, 256])
    NEGATE_CHOICES = _choices(['red', 'green', 'blue'])
    N_FRAMES_CHOICES = _choices([6, 8, 10, 12, 16, 20, 24, 30, 32])
    DELAY_CHOICES = _delay_choices([2, 4, 6, 8, 10, 12, 16, 20])
    FUZZ_CHOICES = _choices(range(50))
    METHOD_CHOICES = [
        ('hue_rotate', 'Hue Rotate'),
        ('replace_color', 'Replace Color'),
    ]

    resize = models.IntegerField("Resize Image", choices=RESIZE_CHOICES)
    n_frames = models.IntegerField("Number of Frames", choices=N_FRAMES_CHOICES, null=True, default=12)
    delay = models.IntegerField("Animation Speed", default=6, choices=DELAY_CHOICES, null=True)
    method = models.CharField(choices=METHOD_CHOICES, default="hue_rotate", max_length=16)
    negate = models.CharField("Negate Channel", choices=NEGATE_CHOICES, null=True, blank=True, max_length=8)
    replace_color = models.CharField(null=True, blank=True, max_length=32)
    fuzz = models.IntegerField(default=3, choices=FUZZ_CHOICES, null=True)

    sourceimage = models.ForeignKey("SourceImage", on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        new = not self.pk
        super().save(*args, **kwargs)
        if new:
            self.party()

    def party(self):
        data = self.to_json(['resize', 'n_frames', 'delay', 'fuzz', 'method', 'negate', 'replace_color'])
        utils.partify(self.sourceimage.src.path, data)

class SourceImage(BaseModel):
    class Meta:
        ordering = ("name",)
    name = models.CharField(max_length=32,unique=True)
    src = models.ImageField(upload_to="source_images")
    colors = JSONField(default=list,blank=True)
    n_frames = models.IntegerField(default=0)

    @property
    def as_json(self):
        keys = ['id','name','colors','n_frames']
        return {
            **{ key: getattr(self,key) for key in keys },
            'src': self.src.url,
        }

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        self.n_frames = utils.get_n_frames(self.src.path)
        self.colors = utils.get_colros(self.src.path)
        super().save(*args,**kwargs)

    @property
    def filename(self):
        return self.src.path.split('/')[-1]

    @property
    def _variant_path(self):
        return os.path.join(settings.MEDIA_ROOT, ".party", self.filename)

    @property
    def variants(self):
        #! TODO this has two file reads and needs to be replaced
        variants = os.listdir(self._variant_path)
        results = []
        for variant in variants:
            variant_path = self._variant_path+'/'+variant+'/'
            steps = sorted(os.listdir(variant_path))
            steps = [s for s in steps if os.path.isdir(variant_path+s)]
            results.append({
                'name': variant,
                'src': f'{settings.MEDIA_URL}.party/{self.filename}/{variant}/party.gif',
                'steps': [{
                    'name': step,
                    'files': sorted(os.listdir(variant_path+step))
                } for step in steps]
            })
        return results
