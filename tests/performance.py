"""
Profile / test results performance. Contains no real "tests" and must be run manually:

.. code:: bash

    python -m cProfile -o /tmp/profile.out `which nosetests` tests.performance

Requires a working API key.
"""
from elex.parser import api
import unittest

SLOW_ELECTION_DATE = '2012-11-06'


class TestElexPerformance(unittest.TestCase):
    def setUp(self, **kwargs):
        self.election = api.Election(electiondate=SLOW_ELECTION_DATE, testresults=False, liveresults=True, is_test=False)

    def test_results(self):
        self.election.results
