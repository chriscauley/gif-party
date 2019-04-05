from django.contrib import admin
from django.utils.safestring import mark_safe

from server.models import SourceImage

@admin.register(SourceImage)
class SourceImageAdmin(admin.ModelAdmin):
    readonly_fields = ['colors','n_frames']
