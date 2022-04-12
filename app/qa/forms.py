from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Question, Answer


class AskForm(forms.ModelForm):
    '''
    Form for adding questions.
    '''
    class Meta:
        model = Question
        fields = ['title', 'text']


class AnswerForm(forms.ModelForm):
    '''
    Form for adding answers
    '''
    class Meta:
        model = Answer
        fields = ['text']

    def __init__(self, question, *args, **kwargs):
        self.question = question
        super(AnswerForm, self).__init__(*args, **kwargs)

    def clean(self):
        self.cleaned_data['question'] = self.question
        return self.cleaned_data


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')

    def clean(self):
        user = authenticate(username=self.cleaned_data['username'],
                            password=self.cleaned_data['password1'])
        if not user:
            raise ValidationError('Invalid username/password')
        self.cleaned_data['user'] = user
        return self.cleaned_data
