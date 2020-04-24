from django.contrib import admin
from django.utils.safestring import mark_safe

from party.models import SourceImage, PartyImage


def render_src_img(self, obj):
    return mark_safe(f'<img src="{obj.src.url}" width="64" />')


@admin.register(SourceImage)
class SourceImageAdmin(admin.ModelAdmin):
    readonly_fields = ['colors', 'n_frames', 'uploaded_by']
    list_display = ['__str__', 'img', 'visibility', 'created']
    list_editable = ['visibility']
    list_filter = ['visibility']
    img = render_src_img
    img.allow_tags = True


@admin.register(PartyImage)
class PartyImageAdmin(admin.ModelAdmin):
    list_display = ['party_dir', 'replace_color', 'created']
    list_filter = ['sourceimage']
