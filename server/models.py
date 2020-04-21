from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from subprocess import Popen, PIPE

import os
import json
import re

from unrest.models import BaseModel
from party import utils

_choices = lambda a: tuple(zip(a, a))
_delay_choices = lambda a: tuple(zip(a, [f'{int(100/i):d} fps' for i in a]))

class PartyImage(BaseModel):
    NEGATE_CHANNEL_CHOICES = _choices(['red', 'green', 'blue'])
    N_FRAMES_CHOICES = _choices([6, 8, 10, 12, 16, 20, 24, 30, 32])
    DELAY_CHOICES = _delay_choices([2, 4, 6, 8, 10, 12, 16, 20])
    FUZZ_CHOICES = _choices(range(50))
    METHOD_CHOICES = [
        ('hue_rotate', 'Hue Rotate'),
        ('replace_color', 'Replace Color'),
    ]

    n_frames = models.IntegerField("Number of Frames", choices=N_FRAMES_CHOICES, null=True, default=12)
    delay = models.IntegerField("Animation Speed", default=6, choices=DELAY_CHOICES, null=True)
    method = models.CharField(choices=METHOD_CHOICES, default="hue_rotate", max_length=16)
    negate_channel = models.CharField(choices=NEGATE_CHANNEL_CHOICES, null=True, blank=True, max_length=8)
    replace_color = models.CharField(null=True, blank=True, max_length=32)
    fuzz = models.IntegerField(default=3, choices=FUZZ_CHOICES, null=True)

    sourceimage = models.ForeignKey("SourceImage", on_delete=models.CASCADE)

    @property
    def name(self):
        return ''.join(utils.get_args(self.arg_dict))

    @property
    def party_dir(self):
        return f"{self.sourceimage.filename}/{self.name}"

    @property
    def party_exists(self):
        return os.path.exists(os.path.join(settings.MEDIA_ROOT, '.party', self.party_dir))

    def save(self, *args, **kwargs):
        new = not self.pk
        super().save(*args, **kwargs)
        if not self.party_exists:
            print('party time from pi#', self.id, self.party_dir)
            self.party()

    @property
    def arg_dict(self):
        return self.to_json(utils.PARTY_FIELDS)

    @staticmethod
    def get_from_dict(sourceimage_id, kwargs):
        for field in utils.PARTY_FIELDS:
            if PartyImage._meta.get_field(field).null:
                # nullable fields need None to make the filtering unique
                kwargs[field] = kwargs.get(field, None)
        partyimage, new  = PartyImage.objects.get_or_create(sourceimage_id=sourceimage_id, **kwargs)
        return partyimage

    def party(self):
        utils.partify(self.sourceimage.src.path, self.arg_dict)

class SourceImage(BaseModel):
    class Meta:
        ordering = ("name",)
    VISIBILITY_CHOICES = _choices([
        'needs_review', # needs review
        'private', # hidden by uploader
        'public', # bisible for everyone
        'hidden', # by mods
    ])
    name = models.CharField(max_length=32,unique=True)
    src = models.ImageField(upload_to="source_images")
    colors = JSONField(default=list,blank=True)
    n_frames = models.IntegerField(default=0)
    visibility = models.CharField(max_length=16, choices=VISIBILITY_CHOICES, default="unknown")

    @property
    def as_json(self):
        keys = ['id', 'name', 'colors', 'n_frames']
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
        # TODO takes about 1us per variant
        # should probably cache this in redis to avoid having all these directory reads
        results = []
        for partyimage in self.partyimage_set.all():
            variant_path = self._variant_path+'/'+partyimage.name+'/'
            steps = sorted(os.listdir(variant_path))
            steps = [s for s in steps if os.path.isdir(variant_path+s)]
            root_url = f'{settings.MEDIA_URL}.party/{self.filename}/{partyimage.name}/'
            results.append({
                'name': partyimage.name,
                'src': f'{root_url}party.gif',
                'root_url': root_url,
                'steps': [{
                    'name': step,
                    'files': sorted(os.listdir(variant_path+step))
                } for step in steps]
            })
        return results
