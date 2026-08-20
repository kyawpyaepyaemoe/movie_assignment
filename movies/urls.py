from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("<int:movie_id>/edit/", views.edit_movie, name="edit_movie"),
    path("<int:movie_id>/delete/", views.delete_movie, name="delete_movie"),
    path("<int:movie_id>/toggle/", views.toggle_watched, name="toggle_watched"),
    path("watchlist/", views.watchlist, name="watchlist"),
]