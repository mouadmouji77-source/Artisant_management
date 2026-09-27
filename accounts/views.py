from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, ServiceForm, ReviewForm,DemandForm
from .models import UserProfile, Service, Demand, ServiceStatus, Review
from django.db.models import Avg
from django.http import HttpResponseRedirect

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            profile = UserProfile(user=user, type=user_form.cleaned_data['user_type'])
            profile.save()
            login(request, user)
            if profile.type == 'client':
                return redirect('client_services')
            elif profile.type == 'artisan':
                return redirect('artisan_dashboard')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'user_form': user_form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                profile = UserProfile.objects.get(user=user)
                if profile.type == 'client':
                    return redirect('client_services')
                elif profile.type == 'artisan':
                    return redirect('artisan_dashboard')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})



@login_required
def client_dashboard(request):
    return render(request, 'accounts/client_dashboard.html')



@login_required
def artisan_dashboard(request):
    services = Service.objects.filter(artisan=request.user)
    demands = Demand.objects.filter(service__in=services)
    return render(request, 'accounts/artisan_dashboard.html', {'services': services, 'demands': demands})

def user_logout(request):
    logout(request)
    return redirect('login')



@login_required
def publish_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.artisan = request.user
            service.save()
            return redirect('artisan_dashboard')
    else:
        form = ServiceForm()
    return render(request, 'accounts/publish_service.html', {'form': form})





@login_required
def edit_service(request, service_id):
    service = get_object_or_404(Service, id=service_id, artisan=request.user)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            print("Form is valid and has been saved.")
            return redirect('artisan_services')
        else:
            print("Form is invalid:", form.errors)
    else:
        form = ServiceForm(instance=service)
        print("Form loaded with instance data.")

    return render(request, 'accounts/edit_service.html', {'form': form})




@login_required
def delete_service(request, pk):
    service = get_object_or_404(Service, pk=pk, artisan=request.user)
    if request.method == 'POST':
        service.delete()
        return redirect('artisan_dashboard')
    return render(request, 'accounts/delete_service.html', {'service': service})





def client_services(request):
    query = request.GET.get('q', '')
    services = Service.objects.annotate(average_rating=Avg('reviews__rating')).order_by('-average_rating')

    if query:
        services = services.filter(title__icontains=query)

    context = {
        'services': services,
    }
    return render(request, 'accounts/client_services.html', context)




@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect('client_dashboard')
    else:
        user_form = UserRegistrationForm(instance=request.user)
    return render(request, 'accounts/update_profile.html', {'user_form': user_form})





@login_required
def demand_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    reviews = Review.objects.filter(service=service)
    
    if request.method == 'POST':
        form = DemandForm(request.POST)
        if form.is_valid():
            demand = form.save(commit=False)
            demand.service = service
            demand.client = request.user
            demand.save()
            messages.success(request, 'Demand sent successfully!')
            return redirect('client_services')
    else:
        form = DemandForm()

    return render(request, 'accounts/demand_service.html', {
        'service': service,
        'reviews': reviews,
        'form': form
    })




@login_required
def accept_demand(request, demand_id):
    demand = get_object_or_404(Demand, id=demand_id)
    demand.status = 'accepted'
    demand.save()
    messages.success(request, 'Demand accepted successfully!')
    return redirect('artisan_dashboard')




@login_required
def refuse_demand(request, demand_id):
    demand = get_object_or_404(Demand, id=demand_id)
    demand.status = 'refused'
    demand.save()
    messages.success(request, 'Demand refused successfully!')
    return redirect('artisan_dashboard')




@login_required
def service_status_list(request):
    client_demands = Demand.objects.filter(client=request.user)
    return render(request, 'accounts/service_status_list.html', {'client_demands': client_demands})



@login_required
def service_status_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    reviews = Review.objects.filter(service=service)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.service = service
            review.client = request.user
            review.save()
            messages.success(request, 'Review added successfully!')
            return redirect('service_status_detail', service_id=service_id)
    else:
        form = ReviewForm()

    return render(request, 'accounts/service_status_detail.html', {
        'service': service,
        'reviews': reviews,
        'form': form
    })




@login_required
def demand_services(request):
    return render(request, 'accounts/demand_services.html')



@login_required
def artisan_services(request):
    services = Service.objects.filter(artisan=request.user)
    return render(request, 'accounts/artisan_services.html', {'services': services})




from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserUpdateForm, UserProfileUpdateForm

# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserUpdateForm, UserProfileUpdateForm


@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('update_profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileUpdateForm(instance=request.user.userprofile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'accounts/update_profile.html', context)


# accounts/views.py
from django.shortcuts import render

def home(request):
    return render(request, 'accounts/index.html')

def contact(request):
    return render(request, 'accounts/contact.html')

def about(request):
    return render(request, 'accounts/about.html')

def service(request):
    return render(request, 'accounts/service.html')
