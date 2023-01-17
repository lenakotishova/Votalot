from django.forms import modelformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views import generic

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView

from .models import *
from .forms import CommentForm, QuestionForm, ChoiceForm, PollFormSet


class IndexView(generic.ListView, LoginRequiredMixin):
    paginate_by = 2

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # return the latest 5 questions
        return Question.objects.filter(
            pub_date__lte=timezone.now()).order_by('-pub_date')[:50]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_context_data(self, *args, **kwargs):
        cat_data = Choice.objects.all()
        context = super(DetailView, self).get_context_data()
        stuff = get_object_or_404(Question, id=(self.kwargs['pk']))
        total_likes = stuff.total_likes()
        context['total_likes'] = total_likes
        is_liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            is_liked = True
        else:
            is_liked = False
        context['is_liked'] = is_liked
        return context


def like_view(request, pk):
    question = get_object_or_404(Question, id=request.POST.get('question_id'))
    is_liked = False

    if question.likes.filter(id=request.user.id).exists():
        question.likes.remove(request.user)
        is_liked = False

    else:
        question.likes.add(request.user)
        is_liked = True

    return HttpResponseRedirect(reverse('polls:details', args=(question.id,)))


class ResultView(LoginRequiredMixin, generic.DetailView):
    login_url = 'users:login'
    model = Question
    template_name = 'polls/results.html'


class AddCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'polls/add_comment.html'
    # fields = '__all__'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        form.instance.question_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('polls:details', kwargs={'pk': self.object.question.pk})

    # success_url = reverse_lazy('polls:index')


class EditCommentView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'polls/edit_comment.html'

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('polls:details', kwargs={'pk': self.object.question.pk})


class DeleteCommentView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'polls/delete_comment.html'
    # success_url = 'polls:index'

    def get_success_url(self):
        return reverse('polls:details', kwargs={'pk': self.object.question.pk})


@login_required
def result_data(request, pk):
    votedata = []

    question = Question.objects.get(id=pk)
    votes = question.choice_set.all()

    for i in votes:
        votedata.append({i.choice_text: i.votes})

    return JsonResponse(votedata, safe=False)


@login_required(login_url='users:login')
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


@login_required(login_url='users:login')
def create_polls_form_view(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        choice_form = PollFormSet(request.POST, request.FILES)
        if form.is_valid() and choice_form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            for ch_form in choice_form:
                if ch_form.is_valid and ch_form.cleaned_data:
                    choice = ch_form.save(commit=False)
                    choice.question = question
                    choice.save()
            return redirect('polls:details', pk=question.pk)
        else:
            return render(request, 'polls/create_poll.html', {'form': form,
                                                              'choice_form': choice_form, })
    else:
        form = QuestionForm()
        choice_form = PollFormSet(queryset=Choice.objects.none(), )

        return render(request, 'polls/create_poll.html', {'form': form,
                                                          'choice_form': choice_form, })


@login_required(login_url='users:login')
def edit_poll_view(request, pk):
    question = Question.objects.get(id=pk)
    formset = PollFormSet(instance=question)
    question_form = QuestionForm(instance=question)
    if request.method == 'POST':
        formset = PollFormSet(request.POST, instance=question)
        question_form = QuestionForm(request.POST, instance=question)

        if formset.is_valid() and question_form.is_valid():
            listing_instance = formset.save(commit=False)
            question_text = question_form.save(commit=False)
            question_text.save()
            for choice_value in listing_instance:
                choice_value.save()
            return redirect('polls:details', pk=question.pk)
        return render(request, 'polls/edit_poll.html', {'question_form': question_form, 'formset': formset})
    else:

        formset = PollFormSet(instance=question)
        return render(request, 'polls/edit_poll.html', {
            'formset': formset,
            'question_form': question_form,
        })


@login_required(login_url='users:login')
def delete_poll_view(request, pk):
    question = Question.objects.get(id=pk)
    if request.method == "POST":
        question.delete()
        return redirect('polls:index')

    context = {
        'question': question,
    }
    return render(request, 'polls/delete_poll.html', context)
