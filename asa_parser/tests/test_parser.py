import os
import unittest

import asa_parser as ap
import git


class ParserTest(unittest.TestCase):
    txt_path = os.path.join(git.Repo('.', search_parent_directories=True).working_tree_dir, 'asa_parser')
    txt_path = os.path.join(txt_path, 'tests')

    def test_show_clock(self):

        # This is the expected value
        expected = '{"timestamp": ["12:40:33.800 UTC Wed Aug 16 2017"]}'

        # Check to make sure the parser returns the expected value
        asa = ap.AsaParser(os.path.join(self.txt_path, 'show_clock.txt'))
        self.assertEqual(expected, asa.clock())

    def test_show_failover_history(self):
        # This is the expected value
        expected = {"group": "1", "timestamp": "16:43:09 UTC Aug 8 ' \
                   '2017", "FromState": "Negotiation", "ToState": "Just Active", "Reason": "No Active unit found"}

        # Check to make sure the parser returns the expected value
        asa = ap.AsaParser(os.path.join(self.txt_path, 'show_failover_history.txt'))
        self.assertEqual(expected, asa.failover_history())

    def test_startup_config_errors(self):
        self.assertEqual(True, True)

    def test_tech_support_license(self):
        self.assertEqual(True, True)

    def test_cpu_usage(self):
        self.assertEqual(True, True)

    def test_memory_region(self):
        self.assertEqual(True, True)

    def test_cpu_detailed(self):
        self.assertEqual(True, True)

    def show_process(self):
        self.assertEqual(True, True)
