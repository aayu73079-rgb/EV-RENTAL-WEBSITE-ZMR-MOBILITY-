# from django.contrib import admin
from .models import ContactInquiry

# @admin.register(ContactMessage)
# class ContactMessageAdmin(admin.ModelAdmin):
#     list_display = ('name', 'email', 'phone', 'inquiry_type', 'submitted_at')
#     search_fields = ('name', 'email', 'phone')




# test code

from django.contrib import admin
from .models import (
    ContactInquiry, FranchiseApplication, ServiceLocation, 
    VehicleModel, RentalBooking
)


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email','phone', 'inquiry_type', 'created_at', 'is_resolved']
    list_filter = ['inquiry_type', 'is_resolved', 'created_at']
    search_fields = ['name', 'email', 'phone']
    readonly_fields = ['created_at']
    list_editable = ['is_resolved']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Inquiry Details', {
            'fields': ('inquiry_type', 'message', 'is_resolved')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(FranchiseApplication)
class FranchiseApplicationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'preferred_city', 'status', 'created_at']
    list_filter = ['status', 'preferred_city', 'created_at']
    search_fields = ['full_name', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['status']
    
    fieldsets = (
        ('Applicant Information', {
            'fields': ('full_name', 'email', 'phone')
        }),
        ('Franchise Details', {
            'fields': ('preferred_city', 'business_experience', 'investment_capacity')
        }),
        ('Application Status', {
            'fields': ('status', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ServiceLocation)
class ServiceLocationAdmin(admin.ModelAdmin):
    list_display = ['city_name', 'state', 'charging_stations', 'battery_swapping_available', 'is_active']
    list_filter = ['state', 'battery_swapping_available', 'is_active']
    search_fields = ['city_name', 'state', 'address']
    list_editable = ['is_active']
    
    fieldsets = (
        ('Location Details', {
            'fields': ('city_name', 'state', 'address')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'google_maps_link')
        }),
        ('Services', {
            'fields': ('charging_stations', 'battery_swapping_available', 'is_active')
        }),
    )


@admin.register(VehicleModel)
class VehicleModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'vehicle_type', 'daily_rate', 'monthly_rate', 'battery_range', 'is_available']
    list_filter = ['vehicle_type', 'is_available']
    search_fields = ['name', 'description']
    list_editable = ['is_available']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'vehicle_type', 'description', 'image')
        }),
        ('Pricing', {
            'fields': ('daily_rate', 'monthly_rate')
        }),
        ('Specifications', {
            'fields': ('battery_range', 'max_speed', 'charging_time', 'features')
        }),
        ('Availability', {
            'fields': ('is_available',)
        }),
    )


@admin.register(RentalBooking)
class RentalBookingAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'vehicle', 'rental_type', 'start_date', 'end_date', 'total_amount', 'status']
    list_filter = ['status', 'rental_type', 'start_date', 'vehicle__vehicle_type']
    search_fields = ['customer_name', 'customer_email', 'customer_phone']
    readonly_fields = ['created_at', 'updated_at', 'total_amount']
    list_editable = ['status']
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('customer_name', 'customer_email', 'customer_phone')
        }),
        ('Booking Details', {
            'fields': ('vehicle', 'rental_type', 'start_date', 'end_date', 'pickup_location')
        }),
        ('Booking Status', {
            'fields': ('status', 'total_amount', 'special_requirements')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# Customize admin site headers
admin.site.site_header = "ZMR Mobility Admin"
admin.site.site_title = "ZMR Mobility Admin Portal"
admin.site.index_title = "Welcome to ZMR Mobility Administration"