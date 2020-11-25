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

    def test_show_process_cpu_hog(self):
        asa = ap.AsaParser(os.path.join(self.txt_path, 'show_process_cpu_hog.txt'))
        result = asa.show_process_cpu_hog()

        self.assertIn('"Process":', result)

        self.assertIn('"Last Hog":', result)

        self.assertIn('"PC":', result)

        self.assertIn('"Call Stack":', result)

        self.assertIn('"Info":', result)
        #self.assertIn('"text":', result)
        #self.assertIn('["Hardware:   FPR-2130"', result)

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

        # make sure each section appears in the JSON return
        self.assertIn('"CriticalError":', result)

        self.assertIn('"Info":', result)

        self.assertIn('"StarInfo":', result)

        self.assertIn('"Warning":', result)

        # make sure the correct Error information is included
        self.assertIn('"Error": "Inspect configuration of this type exists, first remove"', result)
        self.assertIn('"Error": "that configuration and then add the new configuration"', result)

    def test_tech_support_license(self):
        asa = ap.AsaParser(os.path.join(self.txt_path, 'show_tech_support_license.txt'))
        result = asa.show_tech_support_license()
        self.assertIn('Registration:', result)
        self.assertIn('Handle:', result)
        self.assertIn('License:', result)
        self.assertIn('Description:', result)
        self.assertIn('Count:', result)
        self.assertIn('Version:', result)
        self.assertIn('Status:', result)
        self.assertIn('Reservation', result)

    def test_cpu_usage(self):
        asa = ap.AsaParser(os.path.join(self.txt_path, 'show_cpu_usage.txt'))
        result = asa.show_cpu_usage()
        self.assertIn('CPU utilization for 5 seconds', result)
        self.assertIn('1 minute', result)
        self.assertIn('5 minutes', result)
        #self.assertIn('["CPU utilization for 5 seconds = 1%; 1 minute: 10%; 5 minutes: 52%"', result)

    def test_memory_region(self):
        asa = ap.AsaParser(os.path.join(self.txt_path, 'show_memory_region.txt'))
        result = asa.show_memory_region()
        self.assertIn('"Address":', result)
        self.assertIn('"Address"', result)
        self.assertIn('"Perm"', result)
        self.assertIn('"Offset"', result)
        self.assertIn('"Dev"', result)
        self.assertIn('"Inode"', result)
        self.assertIn('"Pathname"', result)
        self.assertIn('["ASLR enabled, text region fff2b5c000-fff70be33c"', result)

    def test_cpu_detailed(self):
        # create a new text file in the tests directory called show_cpu_detailed.txt
        # this file will contain only the "show cpu detailed" section from the main
        # showtech_primary.txt file.  This is done to separate testing functionality from the
        # main production functionality.
        asa = ap.AsaParser(os.path.join(self.txt_path, 'show_cpu_detailed.txt'))
        result = asa.show_cpu_detailed()

        self.assertIn('"Break down of per-core data path versus control point cpu usage:Core 5 sec 1 min 5 min":',result)
        self.assertIn('"Current control point elapsed versus the maximum control point elapsed for":',result)
        self.assertIn('"CPU utilization of external processes for":', result)
        self.assertIn('"Total CPU utilization for":', result)



    def test_ipsec_stats(self):
        asa = ap.AsaParser(os.path.join(self.txt_path,'show_ipsec_stats.txt'))
        result = asa.ipsec_stats()
        self.assertIn('Outbound', result)
        self.assertIn('Inbound', result)
        self.assertIn('"Protocol failures": "0"', result)
        self.assertIn('"Invalid ICMP Errors rcvd": "0"', result)

    def test_context_details(self):
        asa = ap.AsaParser(os.path.join(self.txt_path, 'show_context_detail.txt'))
        result = asa.show_context_details()
        self.assertIn('System', result)
        self.assertIn('Admin', result)
        self.assertIn('Inside1', result)
        self.assertIn('Inside2', result)
        self.assertIn('Inside6', result)
        self.assertIn('Inside2-6', result)
        self.assertIn('Inside11', result)
        self.assertIn('Inside13', result)
        self.assertIn('Inside14', result)
        self.assertIn('Inside4', result)
        self.assertIn('Inside2-1', result)
        self.assertIn('Inside2-2', result)
        self.assertIn('Inside2-4', result)
        self.assertIn('Null', result)


    def test_traffic(self):
        # create a new text file in the tests directory called show_cpu_detailed.txt
        # this file will contain only the "show cpu detailed" section from the main
        # showtech_primary.txt file.  This is done to separate testing functionality from the
        # main production functionality.
        asa = ap.AsaParser(os.path.join(self.txt_path, 'show_traffic.txt'))
        result = asa.show_traffic()
        self.assertIn('"nlp_int_tap:"', result)
        self.assertIn('"diagnostic:"', result)
        self.assertIn('"inside13:"', result)
        self.assertIn('"outside13:"', result)
        self.assertIn('"inside1:"', result)
        self.assertIn('"outside1:"', result)
        self.assertIn('"inside2:"', result)
        self.assertIn('"outside3:"', result)
        self.assertIn('"inside-6-7-9-10:"', result)
        self.assertIn('"outside-6-7-9-10:"', result)
    def test_interface(self):
        # create a new text file in the tests directory called show_cpu_detailed.txt
        # this file will contain only the "show cpu detailed" section from the main
        # showtech_primary.txt file.  This is done to separate testing functionality from the
        # main production functionality.
        self.assertEqual(True, True)
        asa = ap.AsaParser(os.path.join(self.txt_path, 'show_interface.txt'))
        result = asa.show_interface()
        self.assertIn('"text":', result)
        self.assertIn('["Interface Internal-Data0/1 \\"\\", is up, line protocol is up"', result)

    def test_memory(self):
        # create a new text file in the tests directory called show_memory.txt
        # this file will contain only the "show memory" section from the main
        # showtech_primary.txt file.  This is done to separate testing functionality from the
        # main production functionality.
        asa = ap.AsaParser(os.path.join(self.txt_path, 'show_memory.txt'))
        result = asa.show_memory()
        self.assertIn('"Free memory":', result)
        self.assertIn('"Used memory":', result)
        self.assertIn('"Total memory":', result)

    def test_memory_detail(self):
        # create a new text file in the tests directory called show_memory_detail.txt
        # this file will contain only the "show memory detail" section from the main
        # showtech_primary.txt file.  This is done to separate testing functionality from the
        # main production functionality.
        asa = ap.AsaParser(os.path.join(self.txt_path, 'show_memory_detail.txt'))
        result = asa.show_memory_detail()
        self.assertIn("Heap Memory", result)
        self.assertIn("Free Memory", result)
        self.assertIn("System", result)
        self.assertIn("Used Memory", result)
        self.assertIn("1073741824", result)
        self.assertIn('**', result)
        self.assertIn('196608', result)
        self.assertIn('2095616000', result)
        self.assertIn('91520', result)
        self.assertIn('116764672', result)
        self.assertIn('730662368', result)
        #self.assertIn('"text":', result)
        #self.assertIn('----- allocated memory statistics -----', result)

    def test_show_process(self):
        self.assertEqual(True, True)

    def test_show_kernel_process(self):
        self.assertEqual(True, True)

    def test_show_logging_buffered(self):
        asa = ap.AsaParser(os.path.join(self.txt_path, 'show_logging_buffered.txt'))
        result = asa.show_logging_buffered()
        self.assertIn('"text":', result)
        self.assertIn('["Aug 16 2017 15:35:37 KP-systest-admin : %ASA-4-711004: Task ran for 114 msec, Process = Unicorn Admin Handler, PC = f34bf8f4, Call stack = "', result)

    def test_tech_support_detail(self):
        asa = ap.AsaParser(os.path.join(self.txt_path, 'show_tech-support_detail.txt'))
        result = asa.show_tech_support_detail()
        self.assertIn('"text":', result)
        self.assertIn('["Cisco Adaptive Security Appliance Software Version 101.1(1)71 <system>"', result)

    def test_show_resource_usage_counter_all_1(self):
        asa = ap.AsaParser(os.path.join(self.txt_path, 'show_resource_usage_counter_all_1.txt'))
        result = asa.show_resource_usage_counter_all_1()
        self.assertIn('Resource', result)