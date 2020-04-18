from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include

import unrest.views
from unrest.nopass.views import create as nopass_create

import server.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/nopass/', include('unrest.nopass.urls')),
    path('api/server/SourceImage/', server.views.sourceimage_list),
    path('api/server/SourceImage/<int:object_id>/', server.views.sourceimage_detail),
    path('api/schema/PartyImage/', server.views.partyimage_schema),
    path('api/party/', server.views.party),
    re_path('api/(server)/([^/]+)/$', unrest.views.superuser_api_view),
    path("user.json", unrest.views.user_json),
    path("api/auth/register/", nopass_create),
    re_path('^(?:image|images)/', unrest.views.index),
    re_path('^$', unrest.views.index),
]

if settings.DEBUG:
    from django.views.static import serve
    urlpatterns += [
        re_path(
            r'^media/(?P<path>.*)$',
            serve,
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}
        ),
    ]
