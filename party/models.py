from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.template.defaultfilters import slugify
from subprocess import Popen, PIPE

import os
import json
import re

from unrest.models import BaseModel
from party import utils

_choices = lambda a: tuple(zip(a, a))


class PartyImage(BaseModel):
    NEGATE_CHANNEL_CHOICES = _choices(['red', 'green', 'blue'])
    N_FRAMES_CHOICES = _choices([7, 12, 18])
    FUZZ_CHOICES = _choices(range(50))
    METHOD_CHOICES = [
        ('hue_rotate', 'Hue Rotate'),
        ('replace_color', 'Replace Color'),
    ]

    n_frames = models.IntegerField("Number of Frames", choices=N_FRAMES_CHOICES, null=True, default=7)
    method = models.CharField(choices=METHOD_CHOICES, default="hue_rotate", max_length=16)
    negate_channel = models.CharField(choices=NEGATE_CHANNEL_CHOICES, null=True, blank=True, max_length=8)
    replace_color = models.CharField(null=True, blank=True, max_length=32)
    fuzz = models.IntegerField(default=3, choices=FUZZ_CHOICES, null=True)
    src = models.ImageField(upload_to=".party", null=True, blank=True)

    sourceimage = models.ForeignKey("SourceImage", on_delete=models.CASCADE)

    @property
    def name(self):
        return ''.join(utils.get_args(self.arg_dict))

    @property
    def party_dir(self):
        return f"{self.sourceimage.filename}/{self.name}"

    @property
    def party_exists(self):
        return self.src

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.party_exists:
            print('party time from pi#', self.id, self.party_dir)
            self.party()

    @property
    def arg_dict(self):
        arg_dict = self.to_json(utils.PARTY_FIELDS)
        if not self.sourceimage.is_animated:
            arg_dict['delay'] = utils.DELAY
        return arg_dict

    @staticmethod
    def get_from_dict(sourceimage_id, kwargs):
        kwargs = utils.clean_flagkwargs(kwargs)
        partyimage, new = PartyImage.objects.get_or_create(sourceimage_id=sourceimage_id, **kwargs)
        return partyimage

    def party(self):
        # party has delay added in since delay is optional
        argstr = ''.join(utils.get_args(self.arg_dict))
        og_name = self.sourceimage.filename
        output_filename = og_name + argstr + '.gif'
        output_root = f"pi_{self.id}"

        party_stdout = utils.partify(self.sourceimage.src.path, output_root, self.arg_dict, output_filename)
        output_path = os.path.join(settings.MEDIA_ROOT, '.party', output_root, argstr, output_filename)
        if not os.path.exists(output_path):
            raise NotImplementedError(f"party gif failed to save at {output_path}\nstdout:\n{party_stdout}")
        self.src = output_path.split(settings.MEDIA_ROOT + "/")[1]
        self.save()


class SourceImage(BaseModel):
    class Meta:
        ordering = ("name", )

    VISIBILITY_CHOICES = _choices([
        'needs_review',  # needs review
        'private',  # hidden by uploader
        'public',  # visible for everyone
        'hidden',  # by mods
        'trash',  # should be deleted
    ])
    name = models.CharField(max_length=32)
    src = models.ImageField(upload_to="source_images")
    colors = JSONField(default=list, blank=True)
    n_frames = models.IntegerField(default=0)
    visibility = models.CharField(max_length=16, choices=VISIBILITY_CHOICES, default="needs_review")
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    @property
    def is_animated(self):
        return self.n_frames > 1

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.n_frames = utils.get_n_frames(self.src.path)
        self.colors = utils.get_colors(self.src.path)
        if not self.name:
            self.name = slugify(".".join(self.filename.split('.')[:-1]))
        super().save(*args, **kwargs)

    @property
    def filename(self):
        return self.src.path.split('/')[-1]

    @property
    def _variant_path(self):
        return os.path.join(settings.MEDIA_ROOT, ".party", self.filename)

    def get_variants_for_user(self, user):
        # TODO takes about 1us per variant
        # should probably cache this in redis to avoid having all these directory reads
        results = []
        _ = lambda s: s.replace("#", "%23")
        for partyimage in self.partyimage_set.all():
            src_url = partyimage.src.url
            variant_path = '/'.join(partyimage.src.path.split('/')[:-1])
            root_url = '/'.join(src_url.split('/')[:-1])
            steps = sorted(os.listdir(variant_path))
            steps = [s for s in steps if os.path.isdir(os.path.join(variant_path, s))]
            results.append({
                'id': partyimage.id,
                'name': partyimage.name,
                'src': src_url,
                'root_url': root_url,
                'steps': [{
                    'name': step,
                    'files': [_(s) for s in sorted(os.listdir(os.path.join(variant_path, step)))]
                } for step in steps],
                **partyimage.to_json(utils.PARTY_FIELDS)
            })
        return results

def get_visible_source_images(user):
    by_user = models.Q(uploaded_by=user.id)
    is_public = models.Q(visibility='public')
    sourceimages = SourceImage.objects.filter(by_user | is_public)
    return sourceimages