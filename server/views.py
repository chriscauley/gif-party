from django.http import JsonResponse

from server.forms import PartyImageForm
from server.models import SourceImage, PartyImage
from unrest.views import superuser_api_view
import json

def sourceimage_list(request):
    return JsonResponse({
      'results': [si.as_json for si in SourceImage.objects.all()]
    })

def partyimage_api(request,*args):
    data = json.loads(request.body.decode('utf-8') or "{}")
    if request.method == "POST":
        form = PartyImageForm(data)
        if not form.is_valid():
            raise NotImplemented("Bad data")
    return superuser_api_view(request,*args)

def refresh_party(request,_id):
    partyimage = PartyImage.objects.get(id=_id)
    partyimage.refresh()
    return JsonResponse({})