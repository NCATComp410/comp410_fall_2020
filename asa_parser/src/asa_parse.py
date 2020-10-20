import json
import re
from asa_parser import ShowTech


class AsaParser(ShowTech):
    """Parses an ASA specific show tech"""

    def clock(self):
        """Returns show clock timestamp"""
        return json.dumps({'timestamp': self.get_show_section('clock')})

    def failover_history(self):
        """Returns failover history"""

        # Initialize variables
        fh_list = []         # This will hold the failover info
        timestamp = ''       # Timestamp of the current group information
        group_found = False  # Identifies if parser has found a group

        # --- show failover history ---
        for line in  self.get_show_section('failover history'):
            # Check for a timestamp
            if ' UTC ' in line:
                timestamp = line
                group_found = True
            elif group_found:
                data = re.split(r'\s{2,}', line)[1:]
                fh = {'group': data[0],
                      'timestamp': timestamp,
                      'FromState': data[1],
                      'ToState': data[2],
                      'Reason': data[3]}
                fh_list.append(fh)
                group_found = False
        return json.dumps(fh_list)

    def show_interface(self):
        """Parser for show inteface"""
        return json.dumps({'text': self.get_show_section('interface')})
