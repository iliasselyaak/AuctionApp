from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Row, Layout, Submit
from crispy_forms.bootstrap import FormActions

class Login(forms.Form):

    email = forms.EmailField(
        label = 'Email',
        max_length= 250,
        widget=forms.TextInput(attrs={'autocomplete': 'Email'})
    )

    password = forms.CharField(
        label='Password',
        max_length=250,
        widget=forms.PasswordInput(attrs={'autocomplete': 'password'})
    )

    helper = FormHelper()
    helper.form_id = 'login-form'
    helper.layout = Layout(
        Row('email', css_class="mb-2"),
        Row('password', css_class="mb-2"),
        FormActions(
            Submit('login', 'Log in', css_class="mt-2"),
        )
    )

class SignupForm(forms.Form):
    '''Form for user signup'''

    username = forms.CharField(
        label = 'Username',
        widget=forms.TextInput(
            attrs={
                'autocomplete': 'username',
            }
        )
    )

    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(
            attrs={
                'autocomplete': 'email',
            }
        )
    )

    date_of_birth = forms.DateField(
        label='Date of Birth',
        widget=forms.SelectDateWidget(years=range(1900, 2020)))

    password = forms.CharField(
        label='Password',
        max_length=50,
        widget=forms.PasswordInput(attrs={'autocomplete': 'password'})
    )
    password_confirm = forms.CharField(
        label='Confirm Password',
        max_length=50,
        widget=forms.PasswordInput,
    )

    helper = FormHelper()
    helper.form_id = 'signup-form'
    helper.layout = Layout(
        Row('email', css_class='mb-2'),
        Row('username', css_class='mb-2'),
        Row('date_of_birth', css_class='mb-2'),
        Row('password', css_class='mb-2'),
        Row('password_confirm', css_class='mb-2'),
        FormActions(
            Submit('signup', 'Sign up', css_class="btn-primary"),
            css_class='mt-3'
        )
    )



