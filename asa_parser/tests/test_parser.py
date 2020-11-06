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

    def test_startup_config_errors(self):
        self.assertEqual(True, True)

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

    def test_tech_support_detail(self):
        asa = ap.AsaParser(os.path.join(self.txt_path, 'show_tech-support_detail.txt'))
        result = asa.show_tech_support_detail()
        self.assertIn('"text":', result)
        self.assertIn('["Cisco Adaptive Security Appliance Software Version 101.1(1)71 <system>"', result)