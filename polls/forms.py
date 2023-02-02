from datetime import datetime

from django import forms
from django.forms import ModelForm, TextInput, DateTimeInput, HiddenInput, Textarea
from django.forms.models import inlineformset_factory
from django.forms.models import BaseInlineFormSet
from django.forms import BaseModelFormSet

from . import models
from .models import Question, Choice, Comment


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']
        # exclude = ['author']

        labels = {
            'question_text': 'question:',
        }

        widgets = {
            'question_text': TextInput(attrs={
                'class': 'form-class',
                'maxlength': 25,
            }),
        }


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']
        labels = {
            'choice_text': 'choice',
        }
        widgets = {
            'choice_text': TextInput(attrs={
                'class': 'form-control',

            })}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_body']

        widgets = {
            'comment_body': Textarea(attrs={
                'class': 'form-comment',
            })
        }


PollFormSet = inlineformset_factory(Question,
                                    Choice,
                                    form=ChoiceForm,
                                    fields=('choice_text',),
                                    min_num=2,
                                    extra=8,
                                    max_num=10,
                                    can_delete=True,
                                    validate_min=True,
                                    validate_max=True,
                                    )
