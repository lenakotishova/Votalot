from django.urls import path, include
from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='details'),
    path('<int:pk>/results/', views.ResultView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('<int:pk>/edit/', views.edit_poll_view, name='edit'),
    path('create/', views.create_polls_form_view, name='create'),
    # path('create/', views.CreatePollView.as_view(template_name='polls/create_poll.html'), name='create'),

]
