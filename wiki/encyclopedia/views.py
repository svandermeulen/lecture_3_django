from django.http import HttpResponse
from django.shortcuts import render

from . import util


def index(request):
    return render(
        request,
        "encyclopedia/index.html", {
            "entries": util.list_entries()
        })


def navigate_to_entry(request, entry: str):
    content = util.get_entry(title=entry)
    return render(
        request,
        "encyclopedia/entry.html", {
            "entry": entry,
            "content": util.convert_markdown_to_html(content)
        }
    )
