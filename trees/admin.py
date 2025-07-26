from django.contrib import admin
from .models import Account, Tree, PlantedTree, Profile

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'active')
    list_filter = ('active',)
    search_fields = ('name',)
    filter_horizontal = ('users',)
    actions = ['activate_accounts', 'deactivate_accounts']

    def activate_accounts(self, request, queryset):
        queryset.update(active=True)
    activate_accounts.short_description = "Activate selected accounts"

    def deactivate_accounts(self, request, queryset):
        queryset.update(active=False)
    deactivate_accounts.short_description = "Deactivate selected accounts"

@admin.register(Tree)
class TreeAdmin(admin.ModelAdmin):
    list_display = ('name', 'scientific_name')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.prefetch_related('plantedtree_set')
        return qs

    def changelist_view(self, request, extra_context=None):
        return super().changelist_view(request, extra_context=extra_context)

@admin.register(PlantedTree)
class PlantedTreeAdmin(admin.ModelAdmin):
    list_display = ('tree', 'user', 'account', 'age', 'planted_at')
    list_filter = ('tree', 'user', 'account')
    search_fields = ('user__username', 'tree__name')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'joined')
