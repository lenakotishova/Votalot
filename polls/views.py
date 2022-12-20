from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import *
from django.http import Http404


def index(request):
    latest_question_list = QuQuestion.objects.estion.objects.order_by('-pub_date')[:5]
    return render(request, 'polls/index.html', {
        'latest_question_list': latest_question_list,
    }
                  )


def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404('Question does not exist.')
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    return HttpResponse('This is the results for %s' % question_id)


def vote(request, question_id):
    return HttpResponse('You are voting for %s' % question_id)
