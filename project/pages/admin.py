from django.contrib import admin

from .models import ContentBlock, Page


class ContentBlockInline(admin.StackedInline):
    model = ContentBlock
    extra = 0
    min_num = 1


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    inlines = [ContentBlockInline]
    list_display = ("title", "slug", "base", "shown_in_navbar")
    prepopulated_fields = {"slug": ("title",)}
