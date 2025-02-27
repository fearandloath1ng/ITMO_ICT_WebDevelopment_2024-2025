from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DeleteView, UpdateView
from django.contrib import messages
from .forms import UserRegistrationForm, ReservationForm, ReviewForm
from .models import Hotel, Room, Reservation, Review
from datetime import datetime, timedelta

def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('/login/')
    else:
        form = UserRegistrationForm()

    return render(request, 'signup.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/hotels/')
        else:
            return redirect('/login')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def rooms_list(request, hotel_id):
    rooms = Room.objects.filter(hotel_id=hotel_id)
    return render(request, "hotel/hotel_rooms.html", {"rooms": rooms})

def room_reviews(request, hotel_id, room_id):
    room = Room.objects.get(id=room_id)
    try:
        bookings = Reservation.objects.filter(room=room)
        reviews = Review.objects.filter(reservation__in=bookings)
    except Reservation.DoesNotExist:
        reviews = []
    return render(request, "hotel/room_reviews.html", {"room": room, "reviews": reviews})


@login_required(login_url='/login/')
def book_room(request, hotel_id, room_id):
    room = Room.objects.get(id=room_id)
    user = request.user
    context = {}
    form = ReservationForm(request.POST or None)
    if form.is_valid():
        reservation = form.save(commit=False)
        reservation.user = user
        reservation.room = room
        reservation.save()
        return redirect("bookings")
    else:
        print(form.errors)
    context['form'] = form
    return render(request, "booking/book_room.html", context)

@login_required(login_url='/login/')
def write_review(request, booking_id):
    reservation = Reservation.objects.get(id=booking_id)
    context = {}
    form = ReviewForm(request.POST or None)
    if form.is_valid():
        review = form.save(commit=False)
        review.reservation = reservation
        form.save()
        return redirect('room_reviews', reservation.room.hotel.id, reservation.room.id)
    context['form'] = form
    return render(request, "review/write_review.html", context)

def user_bookings(request):
    bookings = Reservation.objects.filter(user_id=request.user)
    return render(request, 'booking/user_bookings.html', {'bookings': bookings})

def monthly_clients(request, hotel_id):
    last_month = datetime.now() - timedelta(days=30)
    clients = Reservation.objects.filter(start_date__gt=last_month).filter(room__hotel_id=hotel_id)
    return render(request, 'hotel/monthly_clients.html', {'bookings_month': clients})

class HotelListView(ListView):
    model = Hotel
    template_name = "hotel/hotels_list.html"
    context_object_name = "hotels"

class BookingDeleteView(DeleteView):
    model = Reservation
    success_url = "/bookings/" 
    template_name = "booking/booking_delete.html"

class BookingUpdateView(UpdateView):
    model = Reservation
    fields = ['start_date', 'end_date']
    success_url = "/bookings/" 
    template_name = "booking/booking_update.html"
    
