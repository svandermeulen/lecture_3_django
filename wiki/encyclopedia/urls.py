from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search_results"),
    path("new_entry", views.new_entry, name="new_page"),
    path("random", views.get_random_entry, name="random_page"),
    path("<str:entry>", views.navigate_to_entry, name="entry"),
    path("edit/<str:entry>", views.edit_entry, name="edit_page"),
    path("delete/<str:entry>", views.delete_entry, name="delete_page")
]
