from django import forms

from .models import Property


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            "title",
            "property_type",
            "location",
            "address",
            "monthly_rent",
            "security_deposit",
            "description",
            "gender_preference",
            "food_available",
            "wifi_available",
            "parking_available",
            "laundry_available",
            "furnished",
            "contact_number",
            "image",
        ]
        widgets = {
            "address": forms.Textarea(attrs={"rows": 3}),
            "description": forms.Textarea(attrs={"rows": 5}),
        }

    def clean_monthly_rent(self):
        rent = self.cleaned_data["monthly_rent"]
        if rent <= 0:
            raise forms.ValidationError("Please enter a valid monthly rent.")
        return rent
