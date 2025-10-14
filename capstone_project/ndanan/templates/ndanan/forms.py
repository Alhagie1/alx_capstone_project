

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
User = get_user_model()
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget= forms.PasswordInput(attrs={
            "class" :"form-control",
            "placeholder":"password",
        }),
        min_length = 8
    )
    
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class" : "form-cotrol",
            "placeholder" : "password",

        }),
        label="confirm_password"
    )


    class Meta:

        model = User
        fields = ["first_name", "last_name", "role", "email","profile_picture" ]

        widgets = {
            "first_name" : forms.TextInput(attrs={"class" : "form-control"}),
            "last_name" : forms.TextInput(attrs={"class" : "form-control"}),
            "role" : forms.TextInput(attrs={"class": "form-control"}),
            "profile_picture" : forms.FileInput(attrs={"class" : "form-control"}),
        }


    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise ValidationError("Password does not match")
        return confirm_password
    
    def save(self,commit = True):
        user = super().save(commit = False)
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()
        return user

        




