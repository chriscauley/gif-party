from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from subprocess import Popen, PIPE

import os
import json

from unrest.models import BaseModel

def run(args):
    process = Popen(args, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    if stderr:
        raise Exception(stderr.decode("utf-8"))
    return stdout.decode("utf-8")

def partify(src_path, data):
    args = ['bash', 'gifit.sh', src_path, get_short_args(data)]
    args += get_args(data)
    return run(args)


def get_args(data):
    args = []
    if data.get('resize'):
        args += ['-r',data['resize']]
    if data.get('n_frames'):
        args += ['-n',data['n_frames']]
    if data.get('delay'):
        args += ['-d',data['delay']]
    if data.get('fuzz'):
        args += ['-f',data['fuzz']]
    method = data.get('color_method')
    if method == 'hue_rotate':
        args += ['-h']
        # TODO doesn't work with replace color!
        # need to do negate before replace color
        if data.get('negate'):
            args += ['-N',data['negate']]
    if method == 'replace_color':
        args += ['-R', data.get('replace_color')]
    args = [str(arg) for arg in args]
    return args


def get_short_args(data):
    return "".join(get_args(data))


_choices = lambda a: tuple(zip(a, a))

class PartyImage(BaseModel):
    RESIZE_CHOICES = _choices([32, 64, 128, 256])
    NEGATE_CHOICES = _choices(['red', 'green', 'blue'])
    N_FRAMES_CHOICES = _choices([6, 8, 10, 12, 16, 20, 24, 30, 32])
    DELAY_CHOICES = _choices([2, 4, 6, 8, 10, 12, 16, 20])
    FUZZ_CHOICES = _choices(range(50))

    resize = models.IntegerField(choices=RESIZE_CHOICES, null=True)
    negate = models.CharField(choices=NEGATE_CHOICES, null=True, max_length=8)
    n_frames = models.IntegerField(choices=N_FRAMES_CHOICES, null=True)
    replace_color = models.CharField(null=True, max_length=16)
    delay = models.IntegerField(default=6, choices=DELAY_CHOICES, null=True)
    fuzz = models.IntegerField(default=3, choices=FUZZ_CHOICES, null=True)

    sourceimage = models.ForeignKey("SourceImage", on_delete=models.CASCADE)


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
        super().save(*args,**kwargs)
        # need to cache some data from imagemagic
        self.n_frames = len(run(['identify',self.src.path]).strip().split('\n'))

        # get raw histogram
        histogram = run(['convert',self.src.path,"+dither",'-format','%c','histogram:info:'])

        # trim whitespace, remove empty lines
        histogram = [l.strip() for l in histogram.split('\n') if l]

        # sort by most occurrence
        histogram = sorted(
            histogram,
            key=lambda s: int(s.split(':')[0]),
            reverse=True
        )

        # ignore zero alpha
        histogram = [l for l in histogram if not ',  0)' in l]

        self.colors = []
        matched = []
        for line in histogram:
            if len(self.colors) > 10:
                break
            count = int(line.split(':')[0])
            color = line.split(' ')[-1]
            if color in matched:
                continue
            matched.append(color)
            self.colors.append({
                'color': color,
                'count': count,
            })
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
