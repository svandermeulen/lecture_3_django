import random

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.forms import Form, CharField, Textarea
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from . import util

from .util import summarize_entry, get_entry


class NewEntryForm(Form):
    title = CharField(label="Title")
    content = CharField(widget=Textarea, label="Content")


def index(request):
    query = request.GET.get("q")
    if query is not None:
        return search(request, query=query)

    entries = [{"title": e, "summary": summarize_entry(get_entry(e))} for e in util.list_entries()]

    return render(
        request,
        "encyclopedia/index.html", {
            "entries": entries,
            "title": "All Pages"
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
    entries_substring = [{"title": e, "summary": summarize_entry(get_entry(e))} for e in entries_substring]
    return render(
        request,
        "encyclopedia/index.html", {
            "title": f"Search Results for '{query}'",
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
                'content': 'Content'
            }
        )
    })


def edit_entry(request, entry):
    if request.method == "POST":
        form = NewEntryForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            path_save = f'entries/{title}.md'
            if default_storage.exists(path_save):
                default_storage.delete(path_save)  # Delete to simulate overwriting
            path_save = default_storage.save(path_save, ContentFile(content))
            assert default_storage.exists(path_save), f"{path_save} is not correctly saved"
            return redirect("wiki:entry", entry=entry)

        return render(
            request,
            "encyclopedia/edit_entry.html", {
                "entry": entry,
                "form": form
            }
        )

    content = util.get_entry(title=entry)

    if content is None:
        raise Http404()

    return render(
        request,
        "encyclopedia/edit_entry.html", {
            "entry": entry,
            "form": NewEntryForm(
                initial={
                    'title': entry,
                    'content': content
                }
            )
        })


def delete_entry(request, entry):
    if request.method == "POST":
        path_entry = f'entries/{entry}.md'
        if default_storage.exists(path_entry):
            default_storage.delete(path_entry)
        return redirect('wiki:index')
    return render(request, "encyclopedia/delete_entry.html", {
        "entry": entry
    })


def get_random_entry(request):
    entry = random.choice(util.list_entries())
    return redirect('wiki:entry', entry=entry)
