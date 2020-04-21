from django import forms
from server.models import SourceImage, PartyImage


class PartyImageForm(forms.ModelForm):
    def __init__(self, data, *args, **kwargs):
        self.sourceimage = data and data.pop('sourceimage', None)
        super().__init__(data, *args, **kwargs)

    def save(self, *args, **kwargs):
        # because we have such a unique combination of unique_together kwargs, use the model to get_or_create
        return PartyImage.get_from_dict(self.sourceimage.id, self.cleaned_data)

    def clean(self, *args, **kwargs):
        # certain combinations of options do not make sense. This removes redundant settings
        # TODO this needs to all be moved into get_from_dict
        data = self.cleaned_data
        if data['method'] == 'replace':
            if not data.get('replace_color'):
                raise forms.ValidationError('You must select a color to replace')
            data.pop('negate_channel', None)
        elif data['method'] == 'rotate':
            data.pop('replace_color', None)
            data.pop('fuzz', None)
        # for now just hard code this since its fixed on front end
        data['n_frames'] = data.get('n_frames') or 12
        return data

    class Meta:
        model = PartyImage
        fields = ('delay', 'method', 'negate_channel', 'replace_color', 'fuzz',)
