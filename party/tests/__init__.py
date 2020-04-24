from django.test import TestCase

from .utils import PartyUtilsTestCase
from party.admin import render_src_img

class E:
    pass


class UtilsTestCase(TestCase):
  def test_render_src_img(self):
    obj = E()
    obj.src = E()
    obj.src.url = "foo"
    self.assertEqual(render_src_img(None, obj), '<img src="foo" width="64" />')
