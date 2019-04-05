from django import forms
from server.models import SourceImage

def zip2(choices):
    return zip(choices,choices)



class PartyImageForm(forms.Form):
    resize = forms.IntegerField(required=False)
    NEGATE_CHOICES = zip2(['','red','green','blue'])
    negate = forms.ChoiceField(required=False,choices=NEGATE_CHOICES)
    n_frames = forms.IntegerField(required=False)
    METHOD_CHOICES = zip2(['hue_rotate','replace_color'])
    color_method = forms.ChoiceField(required=True,choices=METHOD_CHOICES)
    replace_color = forms.CharField(max_length=20,required=False)
    source = forms.ModelChoiceField(queryset=SourceImage.objects.all())
    delay = forms.IntegerField(required=False)