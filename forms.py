# from django import forms
# from .models import ContactMessage

# class ContactForm(forms.ModelForm):
#     class Meta:
#         model = ContactMessage
#         fields = ['name', 'email', 'phone', 'inquiry_type', 'message']
#         widgets = {
#             'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
#             'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
#             'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Phone Number'}),
#             'inquiry_type': forms.Select(attrs={'class': 'form-control'}),
#             'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message or Questions', 'rows': 4}),
#         }





# test code
from django import forms
from .models import ContactInquiry, FranchiseApplication, RentalBooking


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactInquiry
        fields = ['name', 'email', 'phone', 'inquiry_type', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Email',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Phone Number',
                'required': True
            }),
            'inquiry_type': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Your Message or Questions',
                'rows': 5,
                'required': True
            }),
        }


class FranchiseForm(forms.ModelForm):
    class Meta:
        model = FranchiseApplication
        fields = ['full_name', 'email', 'phone', 'preferred_city', 'business_experience']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full Name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number',
                'required': True
            }),
            'preferred_city': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'business_experience': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tell us about your business experience and investment capacity',
                'rows': 4,
                'required': True
            }),
        }


class RentalBookingForm(forms.ModelForm):
    class Meta:
        model = RentalBooking
        fields = [
            'customer_name', 'customer_email', 'customer_phone',
            'vehicle', 'rental_type', 'start_date', 'end_date',
            'pickup_location', 'special_requirements'
        ]
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name'
            }),
            'customer_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Email'
            }),
            'customer_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Phone Number'
            }),
            'vehicle': forms.Select(attrs={'class': 'form-control'}),
            'rental_type': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'pickup_location': forms.Select(attrs={'class': 'form-control'}),
            'special_requirements': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Any special requirements or notes',
                'rows': 3
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date:
            if end_date <= start_date:
                raise forms.ValidationError("End date must be after start date.")
        
        return cleaned_data