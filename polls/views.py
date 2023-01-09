from django.forms import modelformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView

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
        choice_form = PollFormSet(queryset=Choice.objects.none(),)

        return render(request, 'polls/create_poll.html', {'form': form,
                                                          'choice_form': choice_form, })


def edit_poll_view(request, pk):
    question = Question.objects.get(id=pk)
    form = QuestionForm(instance=question)
    choice_form = PollFormSet(instance=question)
    return render(
        request,
        'polls/edit_poll.html',
        {'form': form,
         'choice_form': choice_form, })


# class QuestionInline():
#     form_class = QuestionForm
#     model = Question
#     template_name = "polls/create_form.html"
#
#     # def __init__(self):
#     #     self.object = None
#
#     def form_valid(self, form):
#         named_formsets = self.get_named_formsets()
#         if not all((x.is_valid() for x in named_formsets.values())):
#             return self.render_to_response(self.get_context_data(form=form))
#         form.instance.author = self.request.user
#         self.object = form.save()
#
#         # for every formset, attempt to find a specific formset save function
#         # otherwise, just save.
#         for name, formset in named_formsets.items():
#             formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
#             if formset_save_func is not None:
#                 formset_save_func(formset)
#             else:
#                 formset.save()
#         return redirect('polls:index')
#
#     def formset_choices_valid(self, formset):
#         """
#         Hook for custom formset saving.Useful if you have multiple formsets
#         """
#         choices = formset.save(commit=False)  # self.save_formset(formset, contact)
#         # add this 2 lines, if you have can_delete=True parameter
#         # set in inlineformset_factory func
#         # for obj in formset.deleted_objects:
#         #     obj.delete()
#         for choice in choices:
#             choice.question = self.object
#             choice.save()
#
#     # def formset_images_valid(self, formset):
#     #     """
#     #     Hook for custom formset saving. Useful if you have multiple formsets
#     #     """
#     #     images = formset.save(commit=False)  # self.save_formset(formset, contact)
#     #     # add this 2 lines, if you have can_delete=True parameter
#     #     # set in inlineformset_factory func
#     #     for obj in formset.deleted_objects:
#     #         obj.delete()
#     #     for image in images:
#     #         image.product = self.object
#     #         image.save()
#
#
# class CreatePollView(QuestionInline, CreateView):
#     # template_name = 'polls/create_poll.html'
#     #
#     # model = Question
#     # form_class = QuestionForm
#
#     # sets author to the current user
#     # def form_valid(self, form):
#     #     form.instance.author = self.request.user
#     #     return super().form_valid(form)
#     def get_success_url(self):
#         return reverse('polls:detail', kwargs={'pk': self.object.pk})
#
#     def get_context_data(self, **kwargs):
#         ctx = super(CreatePollView, self).get_context_data(**kwargs)
#         ctx['named_formsets'] = self.get_named_formsets()
#         # if self.request.POST:
#         #     ctx.instance.author = self.request.user
#         #     ctx['form'] = QuestionForm(self.request.POST)
#         #     ctx['inlines'] = PollFormSet(self.request.POST)
#         # else:
#         #     ctx['form'] = QuestionFormSet()
#         #     ctx['inlines'] = PollFormSet()
#         return ctx
#
#     def get_named_formsets(self):
#         if self.request.method == "GET":
#             return {
#                 'poll': PollFormSet(prefix='poll'),
#             }
#         else:
#             return {
#                 'poll': PollFormSet(self.request.POST or None, self.request.FILES or None, prefix='poll'),
#             }
#
#     # def form_valid(self, form):
#     #
#     #     ctx = self.get_context_data()
#     #     inlines = ctx['inlines']
#     #     if inlines.is_valid() and form.is_valid():
#     #         form.instance.author = self.request.user
#     #         self.object = form.save()  # saves Father and Children
#     #         return redirect(self.get_success_url())
#     #     else:
#     #         return self.render_to_response(self.get_context_data(form=form))
#     #
#     # def form_invalid(self, form):
#     #     return self.render_to_response(self.get_context_data(form=form))
#     #
