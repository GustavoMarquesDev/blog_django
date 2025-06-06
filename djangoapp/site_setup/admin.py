from django.contrib import admin
from .models import MenuLink, SiteSetup


# @admin.register(MenuLink)
# class MenuLinkAdmin(admin.ModelAdmin):
#     list_display = 'id', 'text', 'url_or_path'
#     list_display_links = 'id', 'text', 'url_or_path'
#     search_fields = 'id', 'text', 'url_or_path'


class MenuLinkInline(admin.TabularInline):
    model = MenuLink
    extra = 1


@admin.register(SiteSetup)
class SiteSetupAdmin(admin.ModelAdmin):
    list_display = 'title', 'description'
    inlines = [MenuLinkInline]

    # para não permitir que o usuário adicione novos registros apenas uma vez
    def has_add_permission(self, request):

        return not SiteSetup.objects.exists()
