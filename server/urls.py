from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include

from unrest import views as unrest_views
from unrest.user import views as user_views
from unrest.nopass.views import create as nopass_create

import party.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/nopass/', include('unrest.nopass.urls')),
    path('api/server/SourceImage/', party.views.sourceimage_list),
    path('api/server/SourceImage/<int:object_id>/', party.views.sourceimage_detail),
    path('api/schema/PartyImage/', party.views.partyimage_schema),
    path('api/PartyImage/', party.views.post_partyimage),
    path('api/schema/SourceImage/', party.views.sourceimage_schema),
    path('api/SourceImage/', party.views.post_sourceimage),
    path("api/auth/register/", nopass_create),
    re_path('^(?:image|images|login|logout|signup|new)/', unrest_views.index),
    re_path('^$', unrest_views.index),


    path("api/user.json", unrest_views.user_json),
    path('api/login/', user_views.login_ajax),
    path('api/signup/', user_views.signup_ajax),
    path('api/logout/', user_views.logout_ajax),
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
