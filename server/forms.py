from django import forms
from server.models import SourceImage, PartyImage


class PartyImageForm(forms.ModelForm):
    def __init__(self, data, *args, **kwargs):
        self.sourceimage = data and data.pop('sourceimage', None)
        super().__init__(data, *args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.sourceimage_id = self.sourceimage.id
        return super().save(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = self.cleaned_data
        if data['method'] == 'replace':
            if not data.get('replace_color'):
                raise forms.ValidationError('You must select a color to replace')
            data.pop('negate', None)
        elif data['method'] == 'rotate':
            data.pop('replace_color', None)
            data.pop('fuzz', None)
        return data

    class Meta:
        model = PartyImage
        fields = ('resize', 'delay', 'n_frames', 'method', 'negate', 'replace_color', 'fuzz',)
