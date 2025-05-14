from django.urls import path
from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static

from . import views

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
    path("admin/admin_view/", views.admin_view, name="admin_view"),
    path("candidates/", views.main_page, name="main_page"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)