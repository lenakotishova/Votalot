from datetime import datetime

from django import forms
from django.forms import ModelForm, TextInput, DateTimeInput, HiddenInput
from django.forms.models import inlineformset_factory
from django.forms.models import BaseInlineFormSet

from . import models
from .models import Question, Choice


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']
        # exclude = ['author']

        widgets = {
            'question_text': TextInput(attrs={
                'class': 'form-control',
                'maxlength': 25,
            }),
        }

        # def check_date(self):
        #     if Question.pub_date < datetime.date.today():
        #         raise ValidationError('Invalid date')
        #     if Question.pub_date > datetime.date.today() + datetime.timedelta(weeks=4):
        #         raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))
        #


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


# class BaseQuestionFormset(BaseInlineFormSet):
#     def add_fields(self, form, index):
#         super(BaseQuestionFormset, self).add_fields(form, index)
#         form.nested = ChoiceForm(
#             instance=form.instance,
#             data=form.data if form.is_bound else None,
#             files=form.files if form.is_bound else None,
#             prefix='choice',
#             extra=1,
#         )
#

PollFormSet = inlineformset_factory(Question, Choice, form=ChoiceForm, fields=('choice_text',),
                                    min_num=2,
                                    extra=8,
                                    max_num=10,
                                    validate_min=True,
                                    validate_max=True)
