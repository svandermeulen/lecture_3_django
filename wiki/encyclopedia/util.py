import re
from typing import Union

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from markdown2 import Markdown


def summarize_entry(entry_content: str) -> str:
    """
    Returns a summary of the content of and entry. It returns the first 5 words of the text (skipping any headings)
    """

    entry_stripped = entry_content.strip("\n")  # Remove trailing newlines
    entry_stripped = re.sub(r"\s{2,}", "\n", entry_stripped).strip("\n")  # Remove trailing spaces

    lines_split = re.split(r"\n|\r", entry_stripped)

    # Skip headers
    if entry_stripped.startswith("#"):
        lines_split = lines_split[1:]

    summary = " ".join(lines_split).split(" ")[:5]

    return f"{' '.join(summary)} ..."


def list_entries() -> list:
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    filenames = [f for f in filenames if f.endswith(".md")]
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title: str, content: str) -> bool:
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))
    return True


def get_entry(title: str) -> Union[str, None]:
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        with default_storage.open(f"entries/{title}.md") as f:
            entry = f.read().decode("utf-8")
        return entry.replace("\r", "")
    except FileNotFoundError:
        return None


def convert_markdown_to_html(markdown_input: str) -> str:

    m = Markdown()
    return m.convert(markdown_input)
