import json
from datauri import DataURI

from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from unrest.decorators import login_required
from unrest.pagination import paginate
from unrest.schema import form_to_schema
from unrest.views import superuser_api_view

from party.forms import PartyImageForm, SourceImageForm
from party.models import SourceImage, get_visible_source_images
from party import utils


def sourceimage_list(request):
    sourceimages = get_visible_source_images(user=request.user)
    process = lambda i: i.to_json(['name', 'id', 'src'])
    return JsonResponse(paginate(sourceimages, process=process, **request.GET))


def sourceimage_detail(request, object_id):
    attrs = ['name', 'id', 'src', 'colors', 'n_frames']
    obj = get_object_or_404(SourceImage, id=object_id)
    result = obj.to_json(attrs)
    result['variants'] = obj.get_variants_for_user(request.user)
    return JsonResponse(result)


def partyimage_schema(request):
    schema = form_to_schema(PartyImageForm(None))
    return JsonResponse({'schema': schema})


def sourceimage_schema(request):
    schema = form_to_schema(SourceImageForm())
    return JsonResponse({'schema': schema, 'post_url': '/api/SourceImage/'})


def post_partyimage(request):
    data = json.loads(request.body.decode('utf-8') or "{}")
    data['sourceimage'] = get_object_or_404(SourceImage, id=data.pop('sourceimage_id'))
    form = PartyImageForm(data)
    if not form.is_valid():
        # TODO should return a json of form errors
        raise NotImplementedError("Bad data")
    # move most this into PartyImage or PartyImageForm
    partyimage = form.save()
    return JsonResponse({})


@login_required
def post_sourceimage(request):
    data = json.loads(request.body.decode('utf-8') or "{}")
    uri = DataURI(data.pop('src'))
    f = ContentFile(uri.data, name=uri.name)
    si = SourceImage(uploaded_by=request.user)
    si.src.save(f.name, f)
    si.save()
    FILES = {'src': f}
    return JsonResponse({'sourceimage_id': si.id})
