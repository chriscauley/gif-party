from django.contrib import admin
from django.utils.html import format_html

from party.models import SourceImage, PartyImage


@admin.register(SourceImage)
class SourceImageAdmin(admin.ModelAdmin):
    readonly_fields = ['colors', 'n_frames', 'uploaded_by']
    list_display = ['__str__', 'img', 'visibility', 'created']
    list_editable = ['visibility']
    list_filter = ['visibility']

    @admin.display(description="Image")
    def img(self, obj):
        return format_html('<img src="{}" width="64" />', obj.src.url)


@admin.register(PartyImage)
class PartyImageAdmin(admin.ModelAdmin):
    list_display = ['party_dir', 'replace_color', 'created']
    list_filter = ['sourceimage']
