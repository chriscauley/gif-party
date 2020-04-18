from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from server.forms import PartyImageForm
from server.models import SourceImage, get_args, get_short_args, partify
from unrest.views import superuser_api_view
import json

def sourceimage_list(request):
    attrs = ['name', 'id', 'src']
    results = [si.to_json(attrs) for si in SourceImage.objects.all()]
    return JsonResponse({ 'results': results })

def sourceimage_detail(request, object_id):
    attrs = ['name', 'id', 'src', 'colors', 'variants']
    result = get_object_or_404(SourceImage, id=object_id).to_json(attrs)
    return JsonResponse(result)

def party(request):
    data = json.loads(request.body.decode('utf-8') or "{}")
    form = PartyImageForm(data)
    if not form.is_valid():
        print(form.errors)
        raise NotImplementedError("Bad data")
    data = form.cleaned_data
    src_path = data['source'].src.path
    args = get_args(data)
    short_args = get_short_args(data)
    output = partify(src_path,data)
    return JsonResponse({
        'code': short_args,
        'output': output,
    })

