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


def partify(src_path, data):
    args = ['bash', 'gifit.sh', src_path, get_short_args(data)]
    args += get_args(data)
    process = Popen(args, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    print(stdout.decode("utf-8"))
    if stderr:
        print(stderr.decode("utf-8"))


def get_args(data):
    args = []
    if data.get('resize'):
        args += ['-r',data['resize']]
    if data.get('negate'):
        args += ['-N',data['negate']]
    if data.get('n_frames'):
        args += ['-n',data['n_frames']]
    if data.get('hue_rotate'):
        args += ['-h']
    args = [str(arg) for arg in args]
    return args


def get_short_args(data):
    return "".join(get_args(data))


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