from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Bus, Passenger, Booking, Wallet
from .forms import UserRegisterForm, UserLoginForm, BusForm, PassengerForm, WalletForm
from .forms import TicketBookingForm


def home(request):
    return render(request, 'myapp/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Wallet.objects.create(user=user, balance=0.00)
            login(request, user)
            return redirect('ticket_booking')
    else:
        form = UserRegisterForm()
    return render(request, 'myapp/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('ticket_booking')
    else:
        form = UserLoginForm()
    return render(request, 'myapp/login.html', {'form': form})

@login_required
def ticket_booking(request):
    # Ensure the wallet exists for the user
    wallet, created = Wallet.objects.get_or_create(user=request.user, defaults={'balance': 0.00})

    if request.method == 'POST':
        source = request.POST.get('source')
        destination = request.POST.get('destination')
        date = request.POST.get('date')
        buses = Bus.objects.filter(source=source, destination=destination, departure_time__date=date)
        return render(request, 'myapp/ticket_booking.html', {'form': TicketBookingForm(), 'buses': buses, 'wallet_balance': wallet.balance})

    return render(request, 'myapp/ticket_booking.html', {'form': TicketBookingForm(), 'wallet_balance': wallet.balance})




@login_required
def book_ticket(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id)
    if request.method == 'POST':
        passenger_form = PassengerForm(request.POST)
        if passenger_form.is_valid():
            passenger = passenger_form.save()
            booking = Booking.objects.create(user=request.user, bus=bus, total_fare=bus.fare)
            booking.passengers.add(passenger)
            bus.available_seats -= 1
            bus.save()
            return redirect('booking_success', booking_id=booking.id)
    else:
        passenger_form = PassengerForm()
    return render(request, 'myapp/book_ticket.html', {'bus': bus, 'form': passenger_form})

@login_required
def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    wallet = Wallet.objects.get(user=request.user)  # Ensure the wallet exists

    return render(request, 'myapp/booking_success.html', {
        'booking': booking,
        'wallet_balance': wallet.balance  # Pass balance to template
    })


@login_required
def add_money(request):
    wallet = get_object_or_404(Wallet, user=request.user)
    if request.method == 'POST':
        form = WalletForm(request.POST, instance=wallet)
        if form.is_valid():
            form.save()
            return redirect('ticket_booking')
    else:
        form = WalletForm(instance=wallet)
    return render(request, 'myapp/add_money.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    buses = Bus.objects.all()
    return render(request, 'myapp/admin_dashboard.html', {'buses': buses})

@user_passes_test(lambda u: u.is_superuser)
def add_bus(request):
    if request.method == 'POST':
        form = BusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = BusForm()
    return render(request, 'myapp/add_bus.html', {'form': form})