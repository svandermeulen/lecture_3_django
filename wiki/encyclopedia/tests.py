from django.test import TestCase

from .util import convert_markdown_to_html, summarize_entry, get_entry


class TestUtil(TestCase):

    def test_convert_markdown_to_html(self):
        html = convert_markdown_to_html("*boo!*")
        self.assertEqual(u'<p><em>boo!</em></p>\n', html)

    def test_summarize_entry(self):
        entry = """
        # Python
        Python is a programming language that can be used both for writing **command-line scripts** or building **web applications**.
        """
        entry_summary = summarize_entry(entry_content=entry)
        self.assertEqual(entry_summary, "Python is a programming language ...")

    def test_summarize_entry_no_header(self):
        entry = """
        Python is a programming language that can be used both for writing **command-line scripts** or building **web applications**.
        """
        entry_summary = summarize_entry(entry_content=entry)
        self.assertEqual(entry_summary, "Python is a programming language ...")

    def test_summarize_entry_html(self):

        entry = get_entry("/test/HTML")
        entry_summary = summarize_entry(entry_content=entry)
        self.assertEqual(entry_summary, "HTML is a markup language ...")
