from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:entry>", views.navigate_to_entry, name="entry")
]
