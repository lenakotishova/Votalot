from django.forms import modelformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.forms import formset_factory
from django.core.exceptions import ValidationError

from .models import *
from .forms import *


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # return the latest 5 questions
        return Question.objects.filter(
            pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except KeyError:
        return render(request, 'polls/detail.html',
                      {'question': question,
                       'error_message': "You didn't select a choice"
                       })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def create_polls_form_view(request):
    choices_formset = modelformset_factory(Choice, form=ChoiceForm, fields=('choice_text',), extra=10)

    if request.method == "POST":
        form = QuestionForm(request.POST)
        choice_form = choices_formset(request.POST, request.FILES)
        if form.is_valid() and choice_form.is_valid():
            form.author = request.user

            question = form.save()
            for ch_form in choice_form:
                choice = ch_form.save(commit=False)
                choice.question = question
                choice.save()
            return redirect('polls:details', pk=question.pk)
        else:
            return render(request, 'polls/create_poll.html', {'form': form,
                                                              'choice_form': choice_form, })
    else:
        form = QuestionForm()
        choice_form = choices_formset(queryset=Choice.objects.none(),)

        return render(request, 'polls/create_poll.html', {'form': form,
                                                          'choice_form': choice_form, })
