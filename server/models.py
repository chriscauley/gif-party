from django.contrib.postgres.fields import JSONField
from django.db import models
from subprocess import Popen, PIPE

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


class SourceImage(models.Model):
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