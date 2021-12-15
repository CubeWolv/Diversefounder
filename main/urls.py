from django.conf.urls import handler400, handler404
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


from .views import (
    dashboard,
    editprofile,
    findstartups,
    projects,
    fundingprofile,
    campaigns,
    createcampaign,
    campaignsettings,
    editreward,
    home,
    updateUser,
    updateCampaign,
    deleteCampaign,
    campaignviewprivate,
    home,
    startups,
    startupsinvestorprofile,
    startupsstartupprofile,
    findinvestors,
    payment,
    privacypolicy,
    cookiepolicy,
    termsofuse,
    search,
    deletereward,
    coaching,
)

# Preload files


urlpatterns = [
    path('', home, name='home'), 
    path('dashboard/editprofile/',
         editprofile, name='editprofile'),
    path('dashboard/', dashboard, name='dashboard'),
    path('projects/', projects, name='projects'),
    path('dashboard/fundingprofile/', fundingprofile, name='fundingprofile'),
    path('dashboard/yourcampaigns/', campaigns, name='campaigns'),
    path('createcampaign/', createcampaign, name='createcampaign'),
    path('createcampaign/edit/<id>/',
      campaignsettings, name="campaignsettings"), 
    path('reward/<id>/',editreward, name="editreward"),
    path('updateUser/',updateUser,name="update-user"),
    path('yourcampaigns/edit/<id>/',updateCampaign, name="campign-update"),
    path('delete/<id>/',deleteCampaign, name="delete"),
    path('delete/reward/<id>/', deletereward ,name="deletereward"),
    path('projects/<id>/<name>/',campaignviewprivate, name='campaignviewprivate'),
    path('projects/<id>/<name>/payment/',payment, name='payment'),
    path('startups/createinvestorprofile/',startupsinvestorprofile, name="startupsinvestorprofile"),
    path('startups/createstartupprofile/',startupsstartupprofile,name="startupsstartupprofile"),
    path('startups/',startups, name='startups'),
    path('startups/investors/',findinvestors, name="investors"),
    path('startups/startups/',findstartups, name="findstartups"),
    path('privacypolicy/',privacypolicy,name="privacypolicy"),
    path('about/cookies/', cookiepolicy, name="cookiepolicy"),
    path('about/termsofuse', termsofuse, name="termsofuse"),
    path('projects/',search,name="search"),
    path('coaching/',coaching ,name='coaching')






]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)


