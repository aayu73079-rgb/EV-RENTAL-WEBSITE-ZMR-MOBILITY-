# from django.db import models

# class ContactMessage(models.Model):
#     INQUIRY_CHOICES = [
#         ('franchise', 'Franchise Opportunity'),
#         ('vehicle', 'Vehicle Purchase'),
#         ('service', 'Service Support'),
#         ('other', 'Other'),
#     ]

#     name = models.CharField(max_length=100)
#     email = models.EmailField()
#     phone = models.CharField(max_length=20)
#     inquiry_type = models.CharField(max_length=50, choices=INQUIRY_CHOICES)
#     message = models.TextField()
#     submitted_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         # return f"{self.name} - {self.inquiry_type}"
#         return self.name



# test code
from django.db import models
from django.utils import timezone


class ContactInquiry(models.Model):
    INQUIRY_TYPES = [
        ('franchise', 'Franchise Opportunity'),
        ('vehicle', 'Vehicle Purchase'),
        ('service', 'Service Support'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    inquiry_type = models.CharField(max_length=20, choices=INQUIRY_TYPES)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_resolved = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Contact Inquiry'
        verbose_name_plural = 'Contact Inquiries'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.get_inquiry_type_display()}"


class FranchiseApplication(models.Model):
    CITIES = [
        ('noida', 'Noida'),
        ('lucknow', 'Lucknow'),
        ('dehradun', 'Dehradun'),
        ('jaipur', 'Jaipur'),
        ('chandigarh', 'Chandigarh'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    preferred_city = models.CharField(max_length=20, choices=CITIES)
    business_experience = models.TextField()
    investment_capacity = models.DecimalField(max_digits=10, decimal_places=2, help_text="Investment capacity in INR")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, help_text="Internal notes for admin")
    
    class Meta:
        verbose_name = 'Franchise Application'
        verbose_name_plural = 'Franchise Applications'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.full_name} - {self.get_preferred_city_display()}"


class ServiceLocation(models.Model):
    city_name = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    charging_stations = models.IntegerField(default=0)
    battery_swapping_available = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    google_maps_link = models.URLField(blank=True)
    
    class Meta:
        verbose_name = 'Service Location'
        verbose_name_plural = 'Service Locations'
        ordering = ['city_name']
    
    def __str__(self):
        return f"{self.city_name}, {self.state}"


class VehicleModel(models.Model):
    VEHICLE_TYPES = [
        ('e2w', 'Electric 2-Wheeler'),
        ('e3w', 'Electric 3-Wheeler'),
        ('e4w', 'Electric 4-Wheeler'),
    ]
    
    name = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_TYPES)
    description = models.TextField()
    daily_rate = models.DecimalField(max_digits=8, decimal_places=2)
    monthly_rate = models.DecimalField(max_digits=8, decimal_places=2)
    battery_range = models.IntegerField(help_text="Range in kilometers")
    max_speed = models.IntegerField(help_text="Maximum speed in km/h")
    charging_time = models.CharField(max_length=50, help_text="e.g., '4-6 hours'")
    features = models.TextField(help_text="Key features, one per line")
    image = models.ImageField(upload_to='vehicles/', blank=True)
    is_available = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Vehicle Model'
        verbose_name_plural = 'Vehicle Models'
        ordering = ['vehicle_type', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_vehicle_type_display()})"


class RentalBooking(models.Model):
    RENTAL_TYPES = [
        ('daily', 'Daily Rental'),
        ('monthly', 'Monthly Rental'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Confirmation'),
        ('confirmed', 'Confirmed'),
        ('active', 'Active Rental'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=15)
    vehicle = models.ForeignKey(VehicleModel, on_delete=models.CASCADE)
    rental_type = models.CharField(max_length=10, choices=RENTAL_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    pickup_location = models.ForeignKey(ServiceLocation, on_delete=models.CASCADE)
    special_requirements = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Rental Booking'
        verbose_name_plural = 'Rental Bookings'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.customer_name} - {self.vehicle.name} ({self.start_date})"