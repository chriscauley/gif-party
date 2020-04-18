from django import forms
from server.models import SourceImage, PartyImage


class PartyImageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.sourceimage = kwargs.pop('source_image', None)
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        instance.sourceimage = self.sourceimage
        return super().save(*args, **kwargs)

    class Meta:
        model = PartyImage
        fields = ('resize', 'negate', 'n_frames', 'replace_color', 'delay', 'fuzz',)