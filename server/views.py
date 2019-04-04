from django.http import JsonResponse

from server.forms import PartyImageForm
from server.models import SourceImage, get_args, get_short_args, partify
from unrest.views import superuser_api_view
import json

def sourceimage_list(request):
    return JsonResponse({
      'results': [si.as_json for si in SourceImage.objects.all()]
    })

def party(request):
    data = json.loads(request.body.decode('utf-8') or "{}")
    form = PartyImageForm(data)
    if not form.is_valid():
        raise NotImplemented("Bad data")
    data = form.cleaned_data
    src_path = data['source'].src.path
    args = get_args(data)
    short_args = get_short_args(data)
    partify(src_path,data)
    return JsonResponse({
        'code': short_args,
    })
