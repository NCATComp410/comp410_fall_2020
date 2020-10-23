import unittest
import asa_parser as ap
import git
import os


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
        expected = '[{"group": "0", "timestamp": "16:43:08 UTC Aug 8 2017", "FromState": "Active Applying Config", ' \
                   '"ToState": "Active Config Applied", "Reason": "No Active unit found"}, {"group": "0", ' \
                   '"timestamp": "16:43:08 UTC Aug 8 2017", "FromState": "Active Config Applied", "ToState": ' \
                   '"Active", "Reason": "No Active unit found"}, {"group": "1", "timestamp": "16:43:09 UTC Aug 8 ' \
                   '2017", "FromState": "Negotiation", "ToState": "Just Active", "Reason": "No Active unit found"}, ' \
                   '{"group": "2", "timestamp": "16:43:09 UTC Aug 8 2017", "FromState": "Disabled", "ToState": ' \
                   '"Negotiation", "Reason": "Failover state check"}, {"group": "1", "timestamp": "16:43:10 UTC Aug 8 ' \
                   '2017", "FromState": "Just Active", "ToState": "Active Drain", "Reason": "No Active unit found"}, ' \
                   '{"group": "1", "timestamp": "16:43:10 UTC Aug 8 2017", "FromState": "Active Drain", "ToState": ' \
                   '"Active Applying Config", "Reason": "No Active unit found"}, {"group": "1", "timestamp": ' \
                   '"16:43:10 UTC Aug 8 2017", "FromState": "Active Applying Config", "ToState": "Active Config ' \
                   'Applied", "Reason": "No Active unit found"}, {"group": "1", "timestamp": "16:43:10 UTC Aug 8 ' \
                   '2017", "FromState": "Active Config Applied", "ToState": "Active", "Reason": "No Active unit ' \
                   'found"}, {"group": "2", "timestamp": "16:43:11 UTC Aug 8 2017", "FromState": "Negotiation", ' \
                   '"ToState": "Just Active", "Reason": "No Active unit found"}, {"group": "2", "timestamp": ' \
                   '"16:43:11 UTC Aug 8 2017", "FromState": "Just Active", "ToState": "Active Drain", "Reason": "No ' \
                   'Active unit found"}, {"group": "2", "timestamp": "16:43:11 UTC Aug 8 2017", "FromState": "Active ' \
                   'Drain", "ToState": "Active Applying Config", "Reason": "No Active unit found"}, {"group": "2", ' \
                   '"timestamp": "16:43:11 UTC Aug 8 2017", "FromState": "Active Applying Config", "ToState": "Active ' \
                   'Config Applied", "Reason": "No Active unit found"}, {"group": "2", "timestamp": "16:43:11 UTC Aug ' \
                   '8 2017", "FromState": "Active Config Applied", "ToState": "Active", "Reason": "No Active unit ' \
                   'found"}, {"group": "2", "timestamp": "17:37:12 UTC Aug 8 2017", "FromState": "Active", ' \
                   '"ToState": "Standby Ready", "Reason": "Other unit wants me Standby"}, {"group": "2", "timestamp": ' \
                   '"14:01:14 UTC Aug 16 2017", "FromState": "Standby Ready", "ToState": "Just Active", ' \
                   '"Reason": "HELLO not heard from mate"}, {"group": "2", "timestamp": "14:01:15 UTC Aug 16 2017", ' \
                   '"FromState": "Just Active", "ToState": "Active Drain", "Reason": "HELLO not heard from mate"}, ' \
                   '{"group": "2", "timestamp": "14:01:15 UTC Aug 16 2017", "FromState": "Active Drain", "ToState": ' \
                   '"Active Applying Config", "Reason": "HELLO not heard from mate"}, {"group": "2", "timestamp": ' \
                   '"14:01:15 UTC Aug 16 2017", "FromState": "Active Applying Config", "ToState": "Active Config ' \
                   'Applied", "Reason": "HELLO not heard from mate"}, {"group": "2", "timestamp": "14:01:15 UTC Aug ' \
                   '16 2017", "FromState": "Active Config Applied", "ToState": "Active", "Reason": "HELLO not heard ' \
                   'from mate"}, {"group": "2", "timestamp": "15:27:30 UTC Aug 16 2017", "FromState": "Active", ' \
                   '"ToState": "Standby Ready", "Reason": "Other unit wants me Standby"}]'

        # Check to make sure the parser returns the expected value
        asa = ap.AsaParser(os.path.join(self.txt_path, 'show_failover_history.txt'))
        self.assertEqual(expected, asa.failover_history())

    def test_support_cpu_hog(self):
        self.assertEqual(True, True)
        
    def test_startup_config_errors(self):
        # create a new text file in the tests directory called show_startup_config_errors.txt
        # this file will contain only the "show startup-config errors" section from the main
        # showtech_primary.txt file.  This is done to separate testing functionality from the
        # main production functionality.
        asa = ap.AsaParser(os.path.join(self.txt_path, 'show_startup_config_errors.txt'))

        # execute the parser and get the result
        # for now this will simply be a list of all the text in the section
        # the return is in JSON format
        result = asa.startup_config_errors()

        # make sure the text section appears in the JSON return
        self.assertIn('"text":', result)

        # check to make sure the first line of the show section is present in the JSON return
        self.assertIn('["Reading from flash..."', result)

    def test_tech_support_license(self):
        self.assertEqual(True, True)

    def test_cpu_usage(self):
        self.assertEqual(True, True)

    def test_memory_region(self):
        self.assertEqual(True, True)

    def test_cpu_detailed(self):
        self.assertEqual(True,True)

    def test_ipsec_stats(self):
        self.assertEqual(True, True)

    def test_context_details(self):
        self.assertEqual(True, True)

    def test_memory(self):
        self.assertEqual(True, True)

    def show_logging_buffered(self):
        self.assertEqual(True, True)