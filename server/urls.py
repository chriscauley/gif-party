from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include

from unrest.views import spa

import party.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/server/SourceImage/', party.views.sourceimage_list),
    path('api/server/SourceImage/<int:object_id>/', party.views.sourceimage_detail),
    path('api/schema/PartyImage/', party.views.partyimage_schema),
    path('api/PartyImage/', party.views.post_partyimage),
    path('api/schema/SourceImage/', party.views.sourceimage_schema),
    path('api/SourceImage/', party.views.post_sourceimage),
    re_path('^(?:image|images|login|new)/', spa),
    re_path('', include('unrest.urls')),
]

if settings.DEBUG:  # pragma: no cover
    from django.views.static import serve
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
            'show_indexes': True
        }),
    ]
