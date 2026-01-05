

# from django.shortcuts import render
# from .models import ContactMessage
# from .forms import ContactForm


# from django.shortcuts import render, redirect



# def base(request):
#     return render(request,"home.html")
# def about(request):
#     return render(request,"about.html")
# def contact(request):
#     return render(request,"contact.html")
# def home(request):
#     return render(request,"home.html")
# def market(request):
#     return render(request,"market.html")
# def services(request):
#     return render(request,"services.html")

# def team(request):
#     return render(request,'team.html')
# def locations(request):
#     return render(request,'services.html')
# def franchise(request):
#     return render(request, "franchise.html") 

# from django.shortcuts import render
# from django.core.mail import send_mail
# from django.conf import settings
# from .models import ContactMessage

# def contact_view(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#         inquiry_type = request.POST.get('inquiry_type')
#         message = request.POST.get('message')

#         # Save in admin
#         contact = ContactMessage.objects.create(
#             name=name,
#             email=email,
#             phone=phone,
#             inquiry_type=inquiry_type,
#             message=message
#         )

#         # Send email
#         subject = f"New Inquiry from {name}"
#         body = f"""
# You have received a new message from your website:

# Name: {name}
# Email: {email}
# Phone: {phone}
# Inquiry Type: {inquiry_type}
# Message:
# {message}
# """
#         send_mail(
#             subject,
#             body,
#             settings.DEFAULT_FROM_EMAIL,
#             [settings.DEFAULT_FROM_EMAIL],  # send to your own email
#             fail_silently=False,
#         )

#         return render(request, 'thank_you.html', {'name': name})

#     return render(request, 'contact.html')

#  test code
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from .models import (
    ContactInquiry, FranchiseApplication, ServiceLocation, 
    VehicleModel, RentalBooking
)
from .forms import ContactForm, FranchiseForm, RentalBookingForm
import json
from django.shortcuts import render



# def base(request):
#     return render(request,"home.html")
# def about(request):
#     return render(request,"about.html")





def home(request):
    """Home page view with all sections"""
    vehicles = VehicleModel.objects.filter(is_available=True)[:3]
    locations = ServiceLocation.objects.filter(is_active=True)
    
    context = {
        'vehicles': vehicles,
        'locations': locations,
    }
    return render(request, 'home.html', context)


def contact_view(request):
    """Handle contact form submission"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_inquiry = form.save()
            
            # Send email notification to admin
            try:
                send_mail(
                    subject=f'New Contact Inquiry - {contact_inquiry.get_inquiry_type_display()}',
                    message=f"""
                    New contact inquiry received:
                    
                    Name: {contact_inquiry.name}
                    Email: {contact_inquiry.email}
                    Phone: {contact_inquiry.phone}
                    Inquiry Type: {contact_inquiry.get_inquiry_type_display()}
                    
                    Message:
                    {contact_inquiry.message}
                    
                    Submitted at: {contact_inquiry.created_at}
                    """,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.DEFAULT_FROM_EMAIL],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Email sending failed: {e}")
            
            messages.success(request, 'Thank you for your inquiry! We will get back to you soon.')
            return redirect('contact_success')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()
    
    return render(request, 'home.html', {'contact_form': form})


def contact_success(request):
    """Contact form success page"""
    return render(request, 'contact_success.html')


def franchise_application(request):
    """Handle franchise application submission"""
    if request.method == 'POST':
        form = FranchiseForm(request.POST)
        if form.is_valid():
            franchise_app = form.save()
            
            # Send email notification
            try:
                send_mail(
                    subject='New Franchise Application - ZMR Mobility',
                    message=f"""
                    New franchise application received:
                    
                    Name: {franchise_app.full_name}
                    Email: {franchise_app.email}
                    Phone: {franchise_app.phone}
                    Preferred City: {franchise_app.get_preferred_city_display()}
                    
                    Business Experience:
                    {franchise_app.business_experience}
                    
                    Submitted at: {franchise_app.created_at}
                    """,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.DEFAULT_FROM_EMAIL],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Email sending failed: {e}")
            
            messages.success(request, 'Your franchise application has been submitted successfully! We will contact you within 24 hours.')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = FranchiseForm()
    
    return render(request, 'home.html', {'franchise_form': form})


def rental_booking(request):
    """Handle rental booking"""
    if request.method == 'POST':
        form = RentalBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            
            # Calculate total amount based on rental type and duration
            vehicle = booking.vehicle
            days = (booking.end_date - booking.start_date).days
            
            if booking.rental_type == 'daily':
                booking.total_amount = vehicle.daily_rate * days
            else:  # monthly
                months = max(1, days // 30)
                booking.total_amount = vehicle.monthly_rate * months
            
            booking.save()
            
            # Send confirmation email
            try:
                send_mail(
                    subject='Rental Booking Confirmation - ZMR Mobility',
                    message=f"""
                    Dear {booking.customer_name},
                    
                    Your rental booking has been received and is pending confirmation.
                    
                    Booking Details:
                    Vehicle: {booking.vehicle.name}
                    Rental Type: {booking.get_rental_type_display()}
                    Start Date: {booking.start_date}
                    End Date: {booking.end_date}
                    Total Amount: ₹{booking.total_amount}
                    Pickup Location: {booking.pickup_location}
                    
                    We will contact you within 24 hours to confirm your booking.
                    
                    Thank you for choosing ZMR Mobility!
                    """,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[booking.customer_email],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Email sending failed: {e}")
            
            messages.success(request, f'Your booking has been submitted! Total amount: ₹{booking.total_amount}. We will contact you for confirmation.')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors in the booking form.')
    else:
        form = RentalBookingForm()
    
    vehicles = VehicleModel.objects.filter(is_available=True)
    locations = ServiceLocation.objects.filter(is_active=True)
    
    context = {
        'rental_form': form,
        'vehicles': vehicles,
        'locations': locations,
    }
    return render(request, 'home.html', context)


class VehicleListView(ListView):
    """List all available vehicles"""
    model = VehicleModel
    template_name = 'vehicles.html'
    context_object_name = 'vehicles'
    queryset = VehicleModel.objects.filter(is_available=True)


class VehicleDetailView(DetailView):
    """Vehicle detail view"""
    model = VehicleModel
    template_name = 'vehicle_detail.html'
    context_object_name = 'vehicle'


@csrf_exempt
def get_vehicle_price(request):
    """AJAX endpoint to get vehicle pricing"""
    if request.method == 'POST':
        data = json.loads(request.body)
        vehicle_id = data.get('vehicle_id')
        rental_type = data.get('rental_type')
        
        try:
            vehicle = VehicleModel.objects.get(id=vehicle_id)
            if rental_type == 'daily':
                price = float(vehicle.daily_rate)
            else:
                price = float(vehicle.monthly_rate)
            
            return JsonResponse({
                'success': True,
                'price': price,
                'vehicle_name': vehicle.name
            })
        except VehicleModel.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Vehicle not found'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})


def services_view(request):
    """Services page"""
    vehicles = VehicleModel.objects.filter(is_available=True)
    locations = ServiceLocation.objects.filter(is_active=True)
    
    context = {
        'vehicles': vehicles,
        'locations': locations,
    }
    return render(request, 'services.html', context)


def locations_view(request):
    """Locations page"""
    locations = ServiceLocation.objects.filter(is_active=True)
    return render(request, 'locations.html', {'locations': locations})