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
        for line in self.get_show_section('failover history'):
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

    def show_process_cpu_hog(self):
        """Parser for process cpu-hog"""
        return json.dumps({'text': self.get_show_section('process cpu-hog')})
        
    def startup_config_errors(self):
        """Parser for show startup-config errors"""
        return json.dumps({'text': self.get_show_section('startup-config errors')})

    def show_tech_support_license(self):
        """Parser for show tech support license"""
        return json.dumps({'text': self.get_show_section('tech-support license')})

    def show_cpu_usage(self):
        """Parser for show cpu usage"""
        return json.dumps({'text': self.get_show_section('cpu usage')})

    def show_memory_region(self):
        """Parser for show_memory region"""
        return json.dumps({'text': self.get_show_section('memory region')})

    def show_cpu_detailed(self):
        """Parser for show cpu detailed"""
        return json.dumps({'text': self.get_show_section('cpu detailed')})

    def ipsec_stats(self):
        """Parser for show ipsec stats"""
        return json.dumps({'stats': self.get_show_section('ipsec stats')})

    def show_memory(self):
        """Parser for show memory"""
        return json.dumps({'text': self.get_show_section('memory')})

    def show_memory_detail(self):
        """Parsesr for show memory detail"""
        return json.dumps({'text': self.get_show_section('memory detail')})

    def show_tech_support_detail(self):
        """Parser for show cpu detailed"""
        return json.dumps({'text': self.get_show_section('tech-support detail')})

    def show_context_details(self):
        """Parser for show context details"""
        return json.dumps({'stats': self.get_show_section('context details')})

    def show_interface(self):
        """Parser for show interface"""
        return json.dumps({'text': self.get_show_section('interface')})

    def show_traffic(self):
        """Parser for show traffic"""
        return json.dumps({'text': self.get_show_section('traffic')})


    def show_process(self):
        """Parser for show process"""
        return json.dumps({'text': self.get_show_section('process')})

	
    def show_logging_buffered(self):
	    """Parser for show show logging buffered"""
	    return json.dumps({'text': self.get_show_section('logging buffered')})

    def show_kernel_process(self):
        """Parser for show kernel process"""
        return json.dumps({'text': self.get_show_section('kernel process')})
