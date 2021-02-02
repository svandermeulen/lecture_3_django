import os

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.forms import Form, CharField, Textarea
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from . import util


# Add a new task:
class NewEntryForm(Form):
    title = CharField(label="Title")
    content = CharField(widget=Textarea, label="Content")


def index(request):
    query = request.GET.get("q")
    if query is not None:
        return search(request, query=query)

    return render(
        request,
        "encyclopedia/index.html", {
            "entries": util.list_entries()
        }
    )


def navigate_to_entry(request, entry: str):

    content = util.get_entry(title=entry)

    if content is None:
        raise Http404()

    return render(
        request,
        "encyclopedia/entry.html", {
            "entry": entry,
            "content": util.convert_markdown_to_html(content)
        }
    )


def search(request, query: str):

    entries = util.list_entries()
    if query in entries:
        return navigate_to_entry(request, entry=query)

    entries_substring = [entry for entry in entries if query.lower() in entry.lower()]
    return render(
        request,
        "encyclopedia/search_results.html", {
            "query": query,
            "entries": entries_substring
        }
    )


def new_entry(request):

    if request.method == "POST":

        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            path_save = f'entries/{title}.md'
            if default_storage.exists(path_save):
                return render(request, "encyclopedia/new_entry.html", {
                    "form": form,
                    "message": "Title already exists"
                })
            path_save = default_storage.save(path_save, ContentFile(content))
            assert default_storage.exists(path_save), f"{path_save} is not correctly saved"
            return HttpResponseRedirect(reverse("wiki:index"))

        return render(request, "encyclopedia/new_entry.html", {
            "form": form,
            "message": ""
        })

    return render(request, "encyclopedia/new_entry.html", {
        "form": NewEntryForm(
            initial={
                'title': 'Title',
                'content': 'Content'}
        )
    })
