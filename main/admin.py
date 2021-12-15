from django.contrib import admin
from .models import Campaign,Comment,update,reward

# Register your models here.

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('campaignName', 'currentdate' ,'fullname','country')
    search_fields = ('name', 'email', 'body')

    def approve_comments(self, request, queryset):
        queryset.update(active=True)


@admin.register(Comment)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('body','campaign','name')

    def approve_comments(self, request, queryset):
        queryset.update(active=True)




@admin.register(update)
class CampaignAdmin(admin.ModelAdmin):
    def approve_comments(self, request, queryset):
        queryset.update(active=True)



@admin.register(reward)
class CampaignAdmin(admin.ModelAdmin):
    list_display =('campaign' ,'title','price')
    def approve_comments(self, request, queryset):
        queryset.update(active=True)
