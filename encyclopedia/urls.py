from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.entry, name="entry"),
    path("search_entry", views.search_entry, name="search_entry"),
    path("add_entry", views.add_entry, name="add_entry"),
    path("randomized_entry", views.randomized_entry, name="randomized_entry"),
    path("edit_entry",views.edit_entry,name="edit_entry")
]
