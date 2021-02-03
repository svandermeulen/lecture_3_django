from django.test import TestCase

# Create your tests here.
from .util import convert_markdown_to_html


class TestUtil(TestCase):

    def test_convert_markdown_to_html(self):

        html = convert_markdown_to_html("*boo!*")
        self.assertEqual(u'<p><em>boo!</em></p>\n', html)
