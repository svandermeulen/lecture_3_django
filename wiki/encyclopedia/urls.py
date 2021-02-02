from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search_results"),
    path("new_entry", views.new_entry, name="new_page"),
    path("<str:entry>", views.navigate_to_entry, name="entry")
]

urlpatterns += staticfiles_urlpatterns()
