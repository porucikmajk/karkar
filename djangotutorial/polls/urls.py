from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    # ex: /polls/
    path("", views.index, name="index"),
    # ex: /polls/5/
    path("<int:question_id>/", views.detail, name="detail"),
    # ex: /polls/5/results/
    path("<int:question_id>/results/", views.results, name="results"),
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
]

app_name = 'polls'
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:question_id>/", views.detail, name="detail"),
    path("<int:question_id>/results/", views.results, name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("login/", views.login_view, name='login'),
    path("register/", views.register_view, name='register'),
    path("logout/", LogoutView.as_view(next_page='polls:index'), name='logout'),
    path("<int:question_id>/reset_voters", views.reset_voters, name="reset_voters"),
]