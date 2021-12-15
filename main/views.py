from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from accounts.forms import Profileform, UserForm
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from django.contrib import messages
from accounts.forms import Profileform, UserForm
from .models import Campaign,Comment,reward,update
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.db.models import  Q
from django.urls import reverse_lazy ,reverse
import urllib
from django.views import View
from django.conf import settings
from django.http import HttpResponse
import requests



import json

import stripe

from django.http import JsonResponse
 
# campaigns=Campaign.objects.filter(campaignName__icontains=q).filter(campaignTagline__icontains=q)
def projects(request):
    q=[]
    user = request.user
    profile = {}
    if request.user.is_authenticated:
        profile = Profile.objects.get(user1=user)
    if 'q' in request.GET:
        q=request.GET['q']
        campaigns=Campaign.objects.filter( Q(campaignName__icontains=q) | Q(campaignTagline__icontains=q) | Q(category__icontains=q) |  Q(fullname__icontains=q))

    elif 'all' in request.GET:
        all=request.GET['all']
        campaigns=Campaign.objects.filter(is_complete=True)


    else:
        campaigns=Campaign.objects.filter(is_complete=True)


    # Pagintion
    paginator=Paginator(campaigns,12)
    page_number=request.GET.get('page')
    posts_obj=paginator.get_page(page_number)
    return render(request, "projects.html", {"campaigns": campaigns ,"q":q ,"profile":profile,'posts':posts_obj})


def search(request):
    q=[]
    if 'q' in request.GET:
        q=request.GET['q']
        campaigns=Campaign.objects.filter( Q(campaignName__icontains=q) | Q(campaignTagline__icontains=q) | Q(category__icontains=q) | Q(fullname__icontains=q))

    elif 'all' in request.GET:
        all=request.GET['all']
        campaigns=Campaign.objects.filter(is_complete=True)


    else:
        campaigns=Campaign.objects.filter(is_complete=True)

        return render(request, "projects.html", {"campaigns": campaigns ,"q":q})


@login_required
def dashboard(request):
    campaigns = Campaign.objects.filter(owner=request.user)
    number_of_campaigns = len(campaigns)
    obj = get_object_or_404(Profile, user1=request.user)
    print(obj.facebook)
    firstname = request.user.first_name
    lastname = request.user.last_name
    email = request.user.email
    user = request.user
    return render(request, "dashboard.html", {'firstname': firstname, 'lastname': lastname, 'email': email, 'user': user, 'profile': obj, "number": number_of_campaigns})


@login_required
def editprofile(request):
    firstname = request.user.first_name
    lastname = request.user.last_name
    obj = get_object_or_404(Profile, user1=request.user)
    print(obj.__dict__)
    profile_form = Profileform(obj.__dict__)
    if request.method == "POST":
        profile_form = Profileform(request.POST, request.FILES, instance=obj)
        if profile_form.is_valid():
            obj.profileimg = profile_form.cleaned_data['profileimg']
            obj.bio = profile_form.cleaned_data['bio']
            obj.country = profile_form.cleaned_data['country']
            obj.website = profile_form.cleaned_data['website']
            obj.istagram = profile_form.cleaned_data['istagram']
            obj.facebook = profile_form.cleaned_data['facebook']
            obj.linkedin = profile_form.cleaned_data['linkedin']
            obj.twitter = profile_form.cleaned_data['twitter']
            obj.save()
            print(obj.bio)
        return redirect("editprofile")
    return render(request, "editprofile.html", {"form": profile_form, "profile": obj, "firstname":firstname, "lastname":lastname})

@login_required
def updateUser(request):
    if request.method == "POST":
        user = request.user
        user.first_name = request.POST.get("fullname")
        user.email = request.POST.get("email")
        user.save()
    return redirect("editprofile")

def home(request):
    user = request.user
    profile = {}
    if request.user.is_authenticated:
        profile = Profile.objects.get(user1=user)
        return redirect(projects)
    return render(request, "home.html",{"profile":profile})


@login_required
def fundingprofile(request):
    user = request.user
    profile = {}
    if request.user.is_authenticated:
        profile = Profile.objects.get(user1=user)
    return render(request, "profiles/fundingprofile.html",{"profile":profile})


@login_required
def campaigns(request):
    user = request.user
    profile = {}
    if request.user.is_authenticated:
        profile = Profile.objects.get(user1=user)
    campaigns = Campaign.objects.filter(owner=request.user)
    return render(request, 'profiles/campaign.html', {"campaigns": campaigns,"profile":profile})

@login_required
def deleteCampaign(request,id):
    campaign = get_object_or_404(Campaign, id=id)
    campaign.delete()
    return redirect("campaigns") 


@login_required
def createcampaign(request):
    user = request.user
    profile = {}
    if request.user.is_authenticated:
        profile = Profile.objects.get(user1=user)
    campaigns = Campaign.objects.filter(owner=request.user)
    campID = 1
    if request.method == "POST":
        print(request.POST)
        campaign = Campaign.objects.create(
            owner=request.user,
            type=request.POST['type'],
            campaignName = request.POST['campname'],
        )
        campID = campaign.id
        campaign.save()
        return redirect("campaignsettings", id=campaign.id)
    return render(request, "campaign/createcampaign.html",{"profile":profile})



#begin here
@login_required
def campaignsettings(request,id):
    firstname = request.user.first_name
    lastname = request.user.last_name
    email = request.user.email
    campaign = get_object_or_404(Campaign, id=id)
    rewards ={}
    if request.user != campaign.owner:
        return redirect('createcampaign')
    obj = get_object_or_404(Profile, user1=request.user)
    if request.method == "POST"  and request.user == campaign.owner and 'basicsettings' in request.POST:
        campaign.fullname=request.POST['fullname'],
        campaign.websiteURL=request.POST['weburl'],
        campaign.country=request.POST['country'],
        campaign.address=request.POST['address'],
        campaign.city=request.POST['city'],
        campaign.zipcode=request.POST['zipcode']
        campaign.save()
        messages.success(request, "Saved successfully" )

    elif request.method == "POST"  and request.user == campaign.owner and 'campaign' in request.POST:
        campaign.campaignTagline = request.POST['camptag']
        campaign.category = request.POST['category']
        campaign.startdate = request.POST['startdate']
        campaign.enddate = request.POST['enddate']
        campaign.save()
        messages.success(request, "Saved successfully" )

    elif request.method == "POST"  and request.user == campaign.owner and 'pitch' in request.POST:
        campaign.campaignName = request.POST['campaignName']
        campaign.pitchFile = request.FILES['profileimage']
        campaign.vidlink = request.POST['vidurl']
        campaign.campaignPitch = request.POST['campaignPitch']
        campaign.save()
        messages.success(request, "Saved successfully" )


    elif request.method == "POST"  and request.user == campaign.owner and 'reward' in request.POST:
        rewards = reward.objects.create(
            campaign=campaign,
            title=request.POST['reward_title'],
            price=request.POST['reward_price'],
            rewarddetails = request.POST['rewarddetails'],
            rewardpicture = request.FILES['rewardpicture'],
            shippinginfo = request.POST['shippinginfo'],
            total_available = request.POST['total_available'],
            year = request.POST['year'],
            month = request.POST['month']
        )
        rewards.save()

    elif request.method == "POST"  and request.user == campaign.owner and 'faq' in request.POST:
        campaign.faqs = request.POST['faqcamp']
        campaign.save()
        messages.success(request, "Saved successfully")



    return render(request, 'campaign/settingscamp.html', {"reward":rewards,"campaign": campaign ,"profile":obj,'email': email, 'firstname': firstname, 'lastname': lastname})


@login_required
def editreward(request, id):
    rewards =get_object_or_404(reward ,id=id)

    if request.method == "POST"  and 'reward' in request.POST:
        rewards.title=request.POST['reward_title']
        rewards.price=request.POST['reward_price']
        rewards.rewarddetails = request.POST['rewarddetails']
        rewards.rewardfile = request.FILES['rewardpicture'],
        rewards.shippinginfo = request.POST['shippinginfo']
        rewards.total_available = request.POST['total_available']
        rewards.year = request.POST['year']
        rewards.month = request.POST['month']

        rewards.save()
        messages.success(request, 'Successfully changed')
    return render(request, 'campaign/editreward.html',{"rewards":rewards} )

def deletereward(request,id):
    rewards = get_object_or_404(reward, id=id)
    rewards.delete()
    messages.success(request, "Successfully Deleted" )
    return redirect("campaignsettings")



@login_required
def updateCampaign(request, id):
    campaign = get_object_or_404(Campaign, id=id)
    if request.method == "POST" and  'profileimage' in request.FILES and request.user == campaign.owner:
        campaignName = request.POST['campname']
        campaignTagline = request.POST['camptag']
        category = request.POST['category']
        startdate = request.POST['startdate']
        pitchCampaignName = request.POST['pitchCampName']
        pitchFile = request.FILES['profileimage']
        vidlink = request.POST['vidurl']
        campaignPitch = request.POST['campaignPitch']
        messages.success(request,'Data has been updated')
    return render(request, "campaign/updateCampaign.html",{"campaign":campaign})

#end here





def campaignviewprivate(request,id,name):
    user = request.user
    profile = {}
    if request.user.is_authenticated:
        profile = Profile.objects.get(user1=user)
        
    campaign = get_object_or_404(Campaign, id=id)
    data = Campaign.objects.get(id =id)
    #comments=Comment.objects.get(all)

    if request.method == 'POST':
        user=request.user
        comment = Comment.objects.create(
            campaign = campaign,
            name = user,
            body = request.POST['commentbody']
            )
        comment.save()
        return HttpResponseRedirect(reverse('campaignviewprivate'))



    return render(request, 'campaignview.html',{"campaign":campaign, "data":data,"profile":profile })






    







#startups

def startups(request):
    user = request.user
    profile = {}
    if request.user.is_authenticated:
        profile = Profile.objects.get(user1=user)
    return render(request, "startups/startups.html" ,{"profile":profile})

def findinvestors(request):
    user = request.user
    profile = {}
    if request.user.is_authenticated:
        profile = Profile.objects.get(user1=user)
    return render(request,"startups/findinvestors.html",{"profile":profile})

def findstartups(request):
    user = request.user
    profile = {}
    if request.user.is_authenticated:
        profile = Profile.objects.get(user1=user)
    return render(request,"startups/findstartups.html",{"profile":profile})


def  startupsinvestorprofile(request):
    user = request.user
    profile = {}
    if request.user.is_authenticated:
        profile = Profile.objects.get(user1=user)
    return render(request, "startups/forms/investorprofile.html",{"profile":profile})

def startupsstartupprofile(request):
    user = request.user
    profile = {}
    if request.user.is_authenticated:
        profile = Profile.objects.get(user1=user)
    return render(request, "startups/forms/startupprofile.html",{"profile":profile})



def error_404(request ,exception):
    return render(request ,'error/404.html')

def privacypolicy(request):
    user = request.user
    profile = {}
    if request.user.is_authenticated:
        profile = Profile.objects.get(user1=user)
    return render(request, "policy/privacypolicy.html",{"profile":profile})

def cookiepolicy(request):
    user = request.user
    profile = {}
    if request.user.is_authenticated:
        profile = Profile.objects.get(user1=user)
    return render(request, "policy/cookie.html",{"profile":profile})


def termsofuse(request):
    user = request.user
    profile = {}
    if request.user.is_authenticated:
        profile = Profile.objects.get(user1=user)
    return render(request, "policy/termsofuse.html",{"profile":profile})


def coaching(request):
    user = request.user
    profile = {}
    if request.user.is_authenticated:
        profile = Profile.objects.get(user1=user)
    return render(request, "coaching.html" ,{"profile":profile})






##############PAYMENT#########################

def payment(request,id,name):
    #firstname = request.user.first_name
    campaign = get_object_or_404(Campaign, id=id)
    data = Campaign.objects.get(id = id)
    return render(request, "payment.html",{"campaign":campaign, "data":data})


#class StripeAuthorizeView(View):

#    def get(self, request):
#        if not self.request.user.is_authenticated:
#            return HttpResponseRedirect(reverse('login'))
#        url = 'https://connect.stripe.com/oauth/authorize'
#        params = {
#            'response_type': 'code',
#            'scope': 'read_write',
#            'client_id': settings.STRIPE_CONNECT_CLIENT_ID,
#            'redirect_uri': f'http://localhost:8000/users/oauth/callback',
#            'return_url':'http://localhost:8000/',
#        }
#        url = f'{url}?{urllib.parse.urlencode(params)}'
#        return redirect(url)



#class StripeAuthorizeCallbackView(View):
#
#   def get(self, request):
#        code = request.GET.get('code')
#        if code:
#            data = {
#                'client_secret': settings.STRIPE_SECRET_KEY,
#                'grant_type': 'authorization_code',
#                'client_id': settings.STRIPE_CONNECT_CLIENT_ID,
#                'code': code
#            }
#            url = 'https://connect.stripe.com/oauth/token'
#            resp = requests.post(url, params=data)
#            #seller data 
#            stripe_user_id = resp.json()['stripe_user_id']
#            stripe_access_token = resp.json()['access_token']
#            seller = Seller.objects.filter(user_id=self.request.user.id).first()
#            seller.stripe_access_token = stripe_access_token
#            seller.stripe_user_id = stripe_user_id
#            seller.save()
#            print(resp.json())

#        return redirect('home')

