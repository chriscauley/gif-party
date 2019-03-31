from django.http import JsonResponse
from server.models import SourceImage

def sourceimage_list(request):
    return JsonResponse({
      'results': [si.as_json for si in SourceImage.objects.all()]
    })