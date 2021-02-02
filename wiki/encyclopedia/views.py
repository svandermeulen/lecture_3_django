from django.http import Http404
from django.shortcuts import render

from . import util


def index(request):
    query = request.GET.get("q")
    if query is not None:
        return search(request, query=query)

    return render(
        request,
        "encyclopedia/index.html", {
            "entries": util.list_entries()
        })


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
    if entries_substring:
        return render(
            request,
            "encyclopedia/search_results.html", {
                "query": query,
                "entries": entries_substring
            }
        )

    return
