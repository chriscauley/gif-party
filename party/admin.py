from django.contrib import admin
from django.utils.safestring import mark_safe

from party.models import SourceImage, PartyImage

@admin.register(SourceImage)
class SourceImageAdmin(admin.ModelAdmin):
    readonly_fields = ['colors','n_frames']
    list_display = ['__str__', 'img', 'visibility']
    list_editable = ['visibility']
    list_filter = ['visibility']
    def img(self, obj):
        return mark_safe(f'<img src="{obj.src.url}" width="64" />')
    img.allow_tags = True

@admin.register(PartyImage)
class PartyImageAdmin(admin.ModelAdmin):
    list_display = ['party_dir', 'replace_color']
    list_filter = ['sourceimage']