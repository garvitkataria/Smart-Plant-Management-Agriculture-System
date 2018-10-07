from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import  UserForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

# Create your views here.

#@csrf_exempt
def login(request):
    print(request.POST, request.GET)
    print(12345)
    form = UserForm()
    #if request.user != None:
    #    return HttpResponseRedirect(reverse('plants:dashboard'))
    if request.POST.get('username') and request.POST.get('password') and request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            print(user)
            auth_login(request, user)
            return HttpResponseRedirect(reverse('plants:dashboard'))
            #return render(request, 'userdashboard.html', context={'username': user.username})
    return render(request, 'index.html', context={'form': form})

def logout_view(request):
    print(741852963)
    logout(request)
    #print (request.user, "request.user")
    return HttpResponseRedirect(reverse('auth_part:login'))

#@csrf_exempt
def create_profile(request):
    error = ""
    if request.method == 'POST':
        print('yoyo')
        userform = UserForm(request.POST)
        #profileform = ProfileForm(request.POST)
        if userform.is_valid() and (len(User.objects.filter(email=request.POST.get('email')))==0):
            print('yoyo2')
            user = User.objects.create_user(**userform.cleaned_data)
            auth_login(request, user)
            return HttpResponseRedirect(reverse('plants:dashboard'))
            #return HttpResponse(status=200)
        else:
            error = "Username or email already in use."
            print(error)

            return render(request, 'register.html', context={'sign_up': True, 'error': error, 'tried': True})
            
    
    userform = UserForm()
    return render(request, 'register.html', context={'sign_up': True, 'error': error})
           
    
