from datetime import datetime

from django import forms
from django.forms import ModelForm, TextInput, DateTimeInput
from rest_framework.exceptions import ValidationError

from . import models
from .models import Question, Choice


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'pub_date']
        widgets = {
            'question_text': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'question',
            }),
            'pub_date': DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control',
                'placeholder': 'date'}),
        }

        # def check_date(self):
        #     if Question.pub_date < datetime.date.today():
        #         raise ValidationError('Invalid date')
        #     if Question.pub_date > datetime.date.today() + datetime.timedelta(weeks=4):
        #         raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))
        #

class PollsChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']
