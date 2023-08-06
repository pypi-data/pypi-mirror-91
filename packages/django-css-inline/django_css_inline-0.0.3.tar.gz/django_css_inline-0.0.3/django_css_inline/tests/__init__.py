import logging
from django.test import TestCase
from django.template import Context, Template

logger = logging.getLogger('django_css_inline')


class DjangoCssInlineTest(TestCase):

    def render_template(self, string, context=None):
        context = context or {}
        context = Context(context)
        return Template(string).render(context)

    def test_css_static(self):
        rendered = self.render_template(
            '{% load css_inline %}'
            '{% css_inline %}'
            '<link rel="stylesheet" href="/static/django_css_inline/test-1.css">'
            '<link rel="stylesheet" href="/static/django_css_inline/test-2.css">'
            '{% end_css_inline %}'
        )
        self.assertEqual(
            rendered,
            """<style type="text/css">/* Django static test 1 */\n\n.test-1 {\n    color: red;\n}\n/* Django static test 2 */\n\n.test-2 {\n    color: green;\n}\n</style>"""
        )

    def test_css_external(self):
        rendered = self.render_template(
            '{% load css_inline %}'
            '{% css_inline %}'
            '<link rel="stylesheet" href="https://static.snoweb.fr/django-css-inline/test-3.css">'
            '{% end_css_inline %}'
        )
        self.assertEqual(
            rendered,
            """<style type="text/css">/* External test 3 */\n\n.test-3 {\n    color: blue;\n}\n</style>"""
        )

    def test_css_gzip(self):
        rendered = self.render_template(
            '{% load css_inline %}'
            '{% css_inline %}'
            '<link rel="stylesheet" href="https://static.snoweb.fr/django-css-inline/test-3.css">'
            '<link rel="stylesheet" href="https://static.snoweb.fr/snowebsvg/dist/css/themes-0.0.24.css">'
            '{% end_css_inline %}'
        )
        import pdb
        pdb.set_trace()
        self.assertEqual(
            rendered,
            """<style type="text/css">/* External test 3 */\n\n.test-3 {\n    color: blue;\n}\n</style><link rel="stylesheet" href="https://static.snoweb.fr/snowebsvg/dist/css/themes-0.0.24.css">"""
        )
