from .models import Address, Review
from django import forms 


class AddressForm(forms.ModelForm):
    class Meta:
        model=Address
        fields=["full_name","email","mobile","city","zip_code","country","address"]
        

class ProductReviewForm(forms.ModelForm):
    class Meta:
        model=Review
        fields='__all__'
        exclude=["review_by","product"]