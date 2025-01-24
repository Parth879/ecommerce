from django import forms
from account.models import Account, UserProfile


class RegistrationForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password...'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password...'}))
    

    class Meta:
        model = Account
        fields = ['first_name','last_name','phone_number','email','password']

    
    def clean(self):
        cleaned_data = super(RegistrationForm,self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Password and confirm password are not Same!")
        
    def __init__(self, *args, **kwargs):
        super(RegistrationForm,self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = "First Name"
        self.fields['last_name'].widget.attrs['placeholder'] = "Last Namme"
        self.fields['phone_number'].widget.attrs['placeholder'] = "Phone Number"
        self.fields['email'].widget.attrs['placeholder'] = "Email"

        for i in self.fields:
            self.fields[i].widget.attrs['class'] = "form-control"

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name','last_name','phone_number','email']

    def __init__(self, *args, **kwargs):
        super(AccountForm,self).__init__(*args, **kwargs)
    
        for i in self.fields:
            self.fields[i].widget.attrs['class'] = "form-control billing-address-name"

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProfileForm,self).__init__(*args, **kwargs)
    
        for i in self.fields:
            self.fields[i].widget.attrs['class'] = "form-control"