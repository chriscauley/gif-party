from django.test import TestCase
from unittest import mock

from party import utils


class PartyUtilsTestCase(TestCase):
  @mock.patch('party.utils.run')
  def test_run(self, run):
    utils.partify('a', 'b', {})
    assert run.called
