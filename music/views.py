from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import TripForm,UserForm
from .models import Trip



def create_trip(request):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        form = TripForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.user=request.user
            trip.save()
            trips = Trip.objects.filter(user=request.user)
            return render(request, 'music/index.html', {'trip': trips})
        context = {
            "form": form,
        }
        return render(request, 'music/create_trip.html', context)


def delete_trip(request, trip_id):
    trip = Trip.objects.get(pk=trip_id)
    trip.delete()
    trips = Trip.objects.filter(user=request.user)
    return render(request, 'music/index.html', {'trip': trips})



def favorite_trip(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)
    try:
        if trip.is_favorite:
            trip.is_favorite = False
        else:
            trip.is_favorite = True
        trip.save()
    except (KeyError, Trip.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        trip = Trip.objects.filter(user=request.user)
        trips=Trip.objects.all()
        query = request.GET.get("q")
        query1=request.GET.get("y")
        if query and query1:
            trips = trips.filter(
                Q(trip_source__icontains=query) &
                Q(trip_dest__icontains=query1)
            ).distinct()
            return render(request, 'music/index.html', {
                'trips': trips,
                
            })
        elif query:
            trips = trips.filter(
                Q(trip_source__icontains=query) 
                
            ).distinct()
            return render(request, 'music/index.html', {
                'trips': trips,
                
            })
        elif query1:
            trips = trips.filter(
                Q(trip_dest__icontains=query1) 
               
            ).distinct()
          
            return render(request, 'music/index.html', {
                'trips': trips,
                
            })
        else:
            return render(request, 'music/index.html', {'trip': trip})


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'music/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                trips = Trip.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'trip': trips})
            else:
                return render(request, 'music/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'music/login.html', {'error_message': 'Invalid login'})
    return render(request, 'music/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                trips = Trip.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'trips': trips})
    context = {
        "form": form,
    }
    return render(request, 'music/register.html', context)

