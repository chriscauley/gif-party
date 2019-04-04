from django import forms
from server.models import SourceImage

class PartyImageForm(forms.Form):
    resize = forms.IntegerField(required=False)
    _nc = ['','red','green','blue']
    NEGATE_CHOICES = zip(_nc,_nc)
    negate = forms.ChoiceField(required=False,choices=NEGATE_CHOICES)
    n_frames = forms.IntegerField(required=False)
    hue_rotate = forms.BooleanField(required=False)
    source = forms.ModelChoiceField(queryset=SourceImage.objects.all())